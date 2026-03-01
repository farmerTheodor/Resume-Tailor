from pydantic import BaseModel, Field
from typing import List


class RankedItem(BaseModel):
    rank: int = Field(
        ...,
        description="A scale of 1-5 of how important this is to the job description relative to the other values. The lowest value will be cut from the resume first.",
    )
    value: str = Field(
        ...,
        description="This is the value that the jinja template will use.",
    )


class Header(BaseModel):
    name: str = Field(..., description="The applicant's full name.")
    phone: str = Field(..., description="The applicant's phone number.")
    email: str = Field(..., description="The applicant's email address.")
    linkedin: str = Field(
        ...,
        description="The applicant's LinkedIn URL (without https://).",
    )
    github: str = Field(
        ...,
        description="The applicant's GitHub URL (without https://).",
    )


class EducationItem(BaseModel):
    institution: str = Field(
        ...,
        description="The name of the university or college.",
    )
    location: str = Field(..., description="City and state of the institution.")
    degree: str = Field(
        ...,
        description="The degree earned, including major and minors.",
    )
    dates: str = Field(
        ...,
        description="The last date of attendance (e.g., May 2021).",
    )


class ExperienceItem(BaseModel):
    role: str = Field(..., description="A singular job title for this company.")
    company: str = Field(
        ...,
        description="The name of the company or organization.",
    )
    location: str = Field(..., description="City and state of the company.")
    dates: str = Field(..., description="The start and end dates of employment.")
    bullets: List[RankedItem] = Field(
        ...,
        description="A list of accomplishments and duties.",
    )


class ProjectItem(BaseModel):
    title: str = Field(..., description="The name of the project.")
    technologies: str = Field(
        ...,
        description="A short comma-separated list of technologies used.",
    )
    dates: str = Field(..., description="The last date a project was worked on.")
    bullets: List[RankedItem] = Field(
        ...,
        description="A list of project features and accomplishments.",
    )


class SkillCategory(BaseModel):
    category_name: str = Field(
        ...,
        description="The overarching category (e.g., Languages, Frameworks).",
    )
    skills: str = Field(
        ...,
        description="A comma-separated list of skills belonging to this category.",
    )


class RequiredFields(BaseModel):
    # Core Template Fields
    header: Header = Field(
        ..., description="The contact information section at the top of the resume."
    )
    education: List[EducationItem] = Field(
        ..., description="A list of educational institutions attended."
    )
    experience: List[ExperienceItem] = Field(
        ..., description="A list of professional work experiences."
    )
    projects: List[ProjectItem] = Field(
        ..., description="A list of personal or academic projects."
    )
    skills: List[SkillCategory] = Field(
        ...,
        description="A list of technical skill categories and the tools within them.",
    )

    # Extra Fields for the Program logic
    target_job_title: str = Field(
        ...,
        description="The title of the job being applied for. Used by the program to optimize bullet points.",
    )
    max_resume_pages: int = Field(
        1,
        description="The maximum allowed pages for the output. Used by the program to determine how many lowest-ranked items to drop.",
    )
