from typing import Optional

from pydantic import BaseModel, Field


class ResumeLine(BaseModel):
    template_resume_line: str = Field(
        ...,
        description="What you want this resume line to look like.",
    )
    substitution_suggestions: list[str] = Field(
        default=[],
        description="Directions on what the LLM can change.",
    )


class WorkProject(BaseModel):
    description: Optional[str] = Field(
        default=None,
        description="Detailed description of the project, including responsibilities, challenges, and outcomes.",
    )
    technologies_used: list[str] = Field(
        ...,
        description="List of technologies, frameworks, and tools used in the project (e.g., 'Python', 'Google Cloud Functions', 'Java').",
    )
    list_of_resume_lines: list[ResumeLine] = Field(
        ...,
        description="Concise, impactful bullet points summarizing achievements for use on a resume.",
    )


class WorkExperience(BaseModel):
    company: str = Field(
        ...,
        description="Name of the company or organization.",
    )
    list_of_titles: list[str] = Field(
        ...,
        description="List of job titles held at the company.",
    )
    city: str = Field(..., description="City where the job was located.")
    region: str = Field(..., description="Province or state where the job was located.")
    start_date: str = Field(..., description="Start date of employment")
    end_date: Optional[str] = Field(
        default=None,
        description="End date of employment. Leave as None if currently employed.",
    )
    list_of_experiences: list[WorkProject] = Field(
        default=[],
        description="List of projects or experiences at this company, each containing a description, technologies used, and resume lines.",
    )
