from pydantic import BaseModel, Field


class Education(BaseModel):
    degree: str = Field(description="Field of study")
    level: str = Field(description="Degree level")
    institution: str = Field(description="Name of the educational institution")
    graduation_date: str = Field(description="Date of graduation")
    location: str = Field(description="Location of the institution")


class Certification(BaseModel):
    certification_name: str = Field(description="Name of the certification")
    year_obtained: str = Field(description="Year the certification was obtained")
    month_obtained: str = Field(description="Month the certification was obtained")


class PersonalInformation(BaseModel):
    name: str = Field(description="Full name of the person")
    reachout_points: dict[str, str] = Field(
        description="Any additional contact information e.g.: address, phone, email, linkedin, github"
    )
    list_of_education: list[Education] = Field(
        description="List of educational qualifications"
    )
    list_of_certifications: list[Certification] = Field(
        description="List of professional certifications"
    )
    list_of_skills: list[str] = Field(
        description="List of technical and professional skills, e.g.: 'Python', 'Docker', 'Kubernetes'"
    )
