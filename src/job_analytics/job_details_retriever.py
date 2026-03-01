from src.llm import get_structured_llm_response
from pydantic import BaseModel, Field


class JobDetails(BaseModel):
    company_name: str = Field(description="Name of the company offering the job")
    position: str = Field(
        description="One and only one Job position or title. If there are multiple positions mentioned in the job description, select the most relevant one to the job description."
    )
    location: str | None = Field(default=None, description="Location of the job")
    compensation: str | None = Field(
        default=None, description="Compensation details for the job"
    )


def get_job_details(
    job_description: str,
) -> JobDetails:

    prompt = DEFAULT_PROMPT.format(job_description=job_description)

    resume_details = get_structured_llm_response(
        prompt=prompt,
        output_format=JobDetails,
    )

    return resume_details


DEFAULT_PROMPT = """
Extract the relevant details from the following job description.

{job_description}
"""
