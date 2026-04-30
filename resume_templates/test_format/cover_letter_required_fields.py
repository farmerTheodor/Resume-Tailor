from pydantic import BaseModel, Field


class RequiredFields(BaseModel):
    company_name: str = Field(
        ...,
        description="The name of the company being applied to.",
    )
    position_title: str = Field(
        ...,
        description="The title of the position being applied for.",
    )
