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


class PersonalProject(BaseModel):
    project_name: str = Field(
        ...,
        description="Name of the personal project.",
    )
    date_last_worked_on: str = Field(
        ...,
        description="Date when the project was last worked on.",
    )
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
