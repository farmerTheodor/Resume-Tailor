from pathlib import Path
import os
import pymupdf

from src.job_analytics import get_job_details, JobDetails
from src.experience import (
    select_experience,
    get_experience,
    get_all_removable_experience,
    remove_experience,
)

from src.resume_output import (
    get_formatted_resume,
    compile_latex_resume,
    get_resume_template,
    ResumeTemplate,
)

OUTPUT_PATH_ENV_VAR = "OUTPUT_PATH"


def get_default_output_path() -> Path:
    return Path(os.getenv(OUTPUT_PATH_ENV_VAR, "/workspace/output"))


def get_default_formatted_output_path() -> Path:
    formatted_path = get_default_output_path() / "formatted_resumes"
    formatted_path.mkdir(parents=True, exist_ok=True)

    return formatted_path


def get_default_compiled_output_path() -> Path:
    compiled_path = get_default_output_path() / "sharable_resumes"
    compiled_path.mkdir(parents=True, exist_ok=True)

    return compiled_path


def tailor_resume_to_job_description(job_description: str, resume_format: Path):
    job_details = get_job_details(job_description)

    resume_file_name = _get_resume_file_name(job_details)

    resume_template = get_resume_template(resume_format)

    list_of_experience = get_experience()
    selected_experience = select_experience(
        list_of_experience, resume_template, job_description
    )
    formatted_resume_path = (
        get_default_formatted_output_path() / f"{resume_file_name}.tex"
    )
    compiled_resume_path = (
        get_default_compiled_output_path() / f"{resume_file_name}.pdf"
    )

    save_and_compile_resume(
        resume_template,
        selected_experience,
        formatted_resume_path,
        compiled_resume_path,
    )

    while (
        len(get_all_removable_experience(selected_experience)) > 0
        and _check_number_of_pages(compiled_resume_path) > 1
    ):
        experience_to_remove = get_all_removable_experience(selected_experience)[-1]

        selected_experience = remove_experience(
            selected_experience, experience_to_remove
        )

        save_and_compile_resume(
            resume_template,
            selected_experience,
            formatted_resume_path,
            compiled_resume_path,
        )


def save_and_compile_resume(
    resume_template: ResumeTemplate,
    selected_experience,
    formatted_resume_path: Path,
    compiled_resume_path: Path,
) -> Path:
    formatted_resume = get_formatted_resume(resume_template, selected_experience)

    with open(formatted_resume_path, "w") as f:
        f.write(formatted_resume)

    compile_latex_resume(formatted_resume, compiled_resume_path)


def _check_number_of_pages(compiled_resume_path: Path) -> int:
    doc = pymupdf.open(compiled_resume_path)
    num_pages = doc.page_count
    doc.close()

    return num_pages


def _get_resume_file_name(job_details: JobDetails) -> str:
    formatted_position = (
        job_details.position.replace(" ", "_").replace("/", "_").lower()
    )
    formatted_company_name = (
        job_details.company_name.replace(" ", "_").replace("/", "_").lower()
    )

    return f"{formatted_position}_for_{formatted_company_name}"


if __name__ == "__main__":
    sample_job_description = """
    Can you make toast? We are looking for the best toast make in the world to join our team. We need someone who can not only
    make advocado toast, but suffer through the hard times of earning just enough to buy the avocados. You will be responsible for
    making toast to the highest standards. Experience with various types of bread is a must. Knowledge of spreads is a plus, but
    not required. Join us at Tster to make the most beautiful toast the world has ever seen. And no the crusts cannot be cut off.
    """
    sample_resume_format = Path("/workspace/resume_templates/test_format")

    tailor_resume_to_job_description(sample_job_description, sample_resume_format)
