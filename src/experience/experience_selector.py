from pydantic import BaseModel

from src.llm import get_structured_llm_response
from src.resume_output.template_loader import ResumeTemplate


def select_experience(
    input_experience: list[BaseModel],
    resume_template: ResumeTemplate,
    job_description: str,
) -> BaseModel:
    prompt = _get_prompt_for_experience_selection(
        input_experience, job_description, resume_template
    )

    selected_experience = get_structured_llm_response(
        prompt=prompt,
        output_format=resume_template.required_fields,
        debug_questions=[],
    )

    return selected_experience


def _get_prompt_for_experience_selection(
    experience: list[BaseModel],
    job_description: str,
    resume_template: ResumeTemplate,
) -> str:

    experience_in_string = _get_experience_list_in_string(experience)

    prompt = DEFAULT_PROMPT.format(
        experience_list=experience_in_string,
        job_description=job_description,
        template_format=resume_template.template_content,
    )

    return prompt


def _get_experience_list_in_string(experience: list[BaseModel]) -> str:
    experience_in_string = "\n\n".join(
        [
            f"{exp.model_dump_json(indent=2, exclude={'list_of_experiences': {'__all__': {'description'}}, 'description': True})}"
            for exp in experience
        ]
    )

    return experience_in_string


DEFAULT_PROMPT = """
## Persona 
- You are an expert hiring manager and recruiter. You live and breathe resumes and job descriptions. 
- You love to help candidates select their experience that best fits the job that they are applying for.
- You do not fabricate anything that is not from the Experience List.
- You are very detail oriented and always follow instructions carefully.
- You do not embelish or add anything that looks like a resume bullet point that is not in the list_of_resume_lines.

## Task
- Understand what the your fellow hiring managers are looking for in the job description provided.
- Use data from the Experience List to fill out the output format. If the output format requires something that is not in the experience list, 
  at best leave it blank. Do not fabricate any information that is not in the experience list. ex. if the output format has a field for "dates" which requires a start and an end date, but the 
  experience list only has a start date, then put the start date and leave the end date blank. Do not make up an end date.
- Keep in mind that the experience you select should be ranked in order of relevance to the job description. So the most relevant experience should be at the top of the list.
- Experience that is listed as together should be kept together. Do not break up experience that is listed as together in the experience list.
- You can use the substitution suggestions to tweak the resume lines to better fit the job description. But do not make any tweaks that are not in the substitution suggestions. 
  If there are no substitution suggestions, do not make any tweaks.
- Do not add any experience that is not in the experience list to satisfy the Job Description. 
- After you select the experience, double check that the experience you selected exists in the experience list.

## Input Data

#### Job Description
Here is the job description. This is the role you should be tailoring the output to get the best match for. 
The Job Description surrounded by '<<<Job Description' and 'Job Description>>>'
<<<Job Description
{job_description}
Job Description>>>

#### Experience List
This is the list of experience that our candidate has provided. Select the most relevant experience for the
job description that fits the output format.
Experience List surrounded by '<<<Experience' and 'Experience>>>'

<<<Experience
{experience_list}
Experience>>>

"""
