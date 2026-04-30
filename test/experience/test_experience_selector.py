import pytest
from pydantic import BaseModel, Field
from pathlib import Path

from test.data.job_description_loader import get_job_description_tests, JobDescription
from test.util.llm_test_harness.custom_criteria import (
    get_score_for_criteria,
    CustomCriteria,
)

from src.experience import get_experience, select_experience
from src.template_output import Template, get_resume_template, TemplateTypes, OutputFormatTypes


def test_select_experience_returns_valid_response():
    input_experience = [
        _DummyInputExperienceModel(
            titles=["software developer"], experience=["built web apps"]
        ),
        _DummyInputExperienceModel(
            titles=["QA engineer"], experience=["tested web apps"]
        ),
    ]
    job_description = (
        "I am looking for someone with experience in testing Javascript and React."
    )

    selected_experience = select_experience(
        input_experience=input_experience,
        template=_get_dummy_resume_template(),
        job_description=job_description,
    )

    assert isinstance(selected_experience, _DummyOutputExperienceModel)
    assert selected_experience.title == "QA engineer"
    assert "tested web apps" in selected_experience.experience[0].lower()


def test_experience_selector_returns_valid_experience_when_simple_description():
    input_experience = get_experience()

    job_description = """
    We are looking for a Data Scientist at DataCorp with experience in machine learning and data analysis
    """

    selected_experience = select_experience(
        input_experience=input_experience,
        template=_get_dummy_resume_template(),
        job_description=job_description,
    )

    expected_schema = selected_experience.model_json_schema()

    criteria = get_score_for_criteria(
        response_text=selected_experience.model_dump_json(),
        assertion_criteria=f"""
        The selected experience should be relevant to the job description. Between "<<<Job Description" and "Job Description>>>" is 
        Everything within the output must be based on the experience listed within "<<<previous experience" and "previous experience>>>".
        The body should be valid json matching the structure dictated by the stuff between "<<<output format" and "output format>>>".
        The values in the response should match the description of the output format "<<<output format" and "output format>>>".   
        
        <<<Job Description:
        {job_description}
        Job Description>>>
        
        <<<output format
        {expected_schema}
        output format>>>
        
        <<<previous experience
        {input_experience}
        previous experience>>>
        """,
    )
    assert criteria.score >= 4, f"{criteria}"


@pytest.mark.parametrize("job_description", get_job_description_tests())
def test_experience_selector_returns_valid_experience_complex_description(
    job_description: JobDescription,
):
    input_experience = get_experience()
    resume_template = get_resume_template(
        Path("/workspace/resume_templates/test_format")
    )
    selected_experience = select_experience(
        input_experience=input_experience,
        template=resume_template,
        job_description=job_description,
    )

    expected_schema = selected_experience.model_json_schema()

    criteria = get_score_for_criteria(
        response_text=selected_experience.model_dump_json(),
        assertion_criteria=f"""
        The selected experience should be relevant to the job description within "<<<Job Description" and "Job Description>>>".
        The selected experience must match something within the "<<<previous experience" and "previous experience>>>" section. 
        Be sure to make sure nothing is made up.
        Should be a valid json matching the structure dictated by the stuff between "<<<output format" and "output format>>>".
        The values in the response should match the description provided by "<<<output format" and "output format>>>" exactly.
        
        <<<Job Description
        {job_description.description}
        Job Description>>>
        
        <<<output format
        {expected_schema}
        output format>>>
        
        <<<previous experience
        {input_experience}
        previous experience>>>
        """,
    )
    assert (
        criteria.score >= 4
    ), f"{criteria}\n\n response: {selected_experience.model_dump_json()}"


class _DummyInputExperienceModel(BaseModel):
    titles: list[str]
    experience: list[str]


class _DummyOutputExperienceModel(BaseModel):
    title: str = Field(description="The job title of the users experience")
    experience: list[str] = Field(
        description="""A list of strings that are resume bullet points that highlight experience with details from their job.
        Ex: 'Salvaged a critical client relationship by independently identifying and pivoting from an underperforming chatbot 
        platform to direct LLM API integration, resulting in a successful project delivery within a tight deadline.'"""
    )


def _get_dummy_resume_template(
    template_path: str = "dummy_template",
    required_fields=_DummyOutputExperienceModel,
    template_content: str = "This is a dummy template",
    output_format_type: OutputFormatTypes = OutputFormatTypes.LATEX,
    template_type: TemplateTypes = TemplateTypes.RESUME,
) -> Template:
    return Template(
        template_path=template_path,
        template_content=template_content,
        required_fields=required_fields,
        output_format_type=output_format_type,
        template_type=template_type,
    )
