from pydantic import BaseModel
from pathlib import Path
import yaml
import pytest


class JobDescription(BaseModel):
    job_title: str
    company: str
    description: str
    location: str | None = None


def get_job_description_tests() -> list[pytest.param]:
    job_descriptions = []
    folder_path = Path("test/data/job_descriptions/")

    for file_name in folder_path.glob("*.yaml"):
        with open(file_name, "r") as file:
            content = yaml.safe_load(file)
            job_description = JobDescription(**content)
            job_descriptions.append(pytest.param(job_description, id=file_name.stem))

    return job_descriptions
