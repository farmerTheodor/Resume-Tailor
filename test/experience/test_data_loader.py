from pathlib import Path
import uuid
import os
import shutil
import pytest
from src.experience import get_experience, PersonalProject
from src.experience.data_loader import (
    EXPERIENCE_DIRECTORY_ENV_VAR,
    TEMPLATE_FILES_TO_IGNORE,
    DEFAULT_EXPERIENCE_DIRECTORY,
)
import yaml


@pytest.fixture
def personal_project_base_object() -> dict:
    return get_default_personal_project_object()


# @pytest.fixture()
# def experience_path(tmp_path: Path) -> Path:
#     for template_file in TEMPLATE_FILES_TO_IGNORE:
#         shutil.copy(Path(DEFAULT_EXPERIENCE_DIRECTORY) / template_file, tmp_path)

#     yield tmp_path
#     os.environ.pop(EXPERIENCE_DIRECTORY_ENV_VAR, None)


def test_load_experience_with_file_that_is_valid(
    tmp_path: Path, personal_project_base_object: dict
):

    temp_file = create_temporary_yaml_file(tmp_path, personal_project_base_object)
    resume_details = get_experience(temp_file)

    assert len(resume_details) == 1
    assert isinstance(resume_details[0], PersonalProject)


def test_load_experience_with_folder_that_is_valid(
    tmp_path: Path, personal_project_base_object: dict
):

    create_temporary_yaml_file(tmp_path, personal_project_base_object)
    create_temporary_yaml_file(tmp_path, personal_project_base_object)
    resume_details = get_experience(tmp_path)

    assert len(resume_details) == 2


def test_load_experience_with_folder_that_contains_invalid_files(
    tmp_path: Path, personal_project_base_object: dict
):

    create_temporary_yaml_file(tmp_path, personal_project_base_object)

    with open(tmp_path / "invalid_file.txt", "w") as file:
        file.write("This is an invalid file and should be ignored.")

    resume_details = get_experience(tmp_path)

    assert len(resume_details) == 1


def create_temporary_yaml_file(tmp_path: Path, content: dict) -> Path:
    file_name = uuid.uuid4()
    file_path = tmp_path / f"{file_name}.yaml"
    with open(file_path, "w") as file:
        yaml.dump(content, file)
    return file_path


def get_default_personal_project_object() -> dict:
    return {
        "project_name": "Sample Project",
        "date_last_worked_on": "2024-01-15",
        "description": "This is a sample project description.",
        "technologies_used": ["Python", "pytest"],
        "list_of_resume_lines": [
            {
                "template_resume_line": "Developed a sample project using Python",
                "substitution_suggestions": ["Change the technology stack as needed"],
            }
        ],
    }
