from pathlib import Path
from pydantic import BaseModel

from src.llm import get_structured_llm_response
from src.template_output import Template, TemplateTypes

RESUME_SELECTION_PROMPT_PATH = (
    Path(__file__).parent / "prompts" / "resume_selection_prompt.md"
)
COVER_LETTER_SELECTION_PROMPT_PATH = (
    Path(__file__).parent / "prompts" / "cover_letter_selection_prompt.md"
)


def select_experience(
    input_experience: list[BaseModel],
    template: Template,
    job_description: str,
) -> BaseModel:
    prompt = _get_prompt_for_experience_selection(
        input_experience, job_description, template
    )

    selected_experience = get_structured_llm_response(
        prompt=prompt,
        output_format=template.required_fields,
        debug_questions=[],
    )

    return selected_experience


def _get_prompt_for_experience_selection(
    experience: list[BaseModel],
    job_description: str,
    template: Template,
) -> str:
    experience_in_string = _get_experience_list_in_string(experience)

    unformatted_prompt = ""
    if template.template_type == TemplateTypes.COVER_LETTER:
        unformatted_prompt = _get_prompt_from_file(COVER_LETTER_SELECTION_PROMPT_PATH)
    elif template.template_type == TemplateTypes.RESUME:
        unformatted_prompt = _get_prompt_from_file(RESUME_SELECTION_PROMPT_PATH)
    else:
        raise ValueError(f"Unsupported template type: {template.template_type}")

    formatted_prompt = unformatted_prompt.format(
        experience_list=experience_in_string,
        job_description=job_description,
        template_format=template.template_content,
    )

    return formatted_prompt


def _get_prompt_from_file(file_path: Path) -> str:
    with open(file_path, "r") as f:
        return f.read()


def _get_experience_list_in_string(experience: list[BaseModel]) -> str:
    experience_in_string = "\n\n".join(
        [
            f"{exp.model_dump_json(indent=2, exclude={'list_of_experiences': {'__all__': {'description'}}, 'description': True})}"
            for exp in experience
        ]
    )

    return experience_in_string
