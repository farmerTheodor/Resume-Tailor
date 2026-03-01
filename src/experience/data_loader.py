from pathlib import Path
from pydantic import BaseModel
import yaml
import os

from .experience_types.personal_information import PersonalInformation
from .experience_types.personal_project import PersonalProject
from .experience_types.work_experience import WorkExperience

# Define the list of supported resume data types
SUPPORTED_DATA_TYPES = WorkExperience | PersonalProject | PersonalInformation
EXPERIENCE_DATA_TYPES: list[SUPPORTED_DATA_TYPES] = [
    WorkExperience,
    PersonalProject,
    PersonalInformation,
]

EXPERIENCE_DIRECTORY_ENV_VAR = "EXPERIENCE_DATA_PATH"
DEFAULT_EXPERIENCE_DIRECTORY = "/workspace/experience"


def get_experience_directory() -> Path:
    return Path(os.getenv(EXPERIENCE_DIRECTORY_ENV_VAR, DEFAULT_EXPERIENCE_DIRECTORY))


TEMPLATE_FILES_TO_IGNORE = [
    "work_experience_template.yaml",
    "personal_project_template.yaml",
    "personal_information_template.yaml",
]


def get_experience(
    experience_path: Path = None,
) -> list[SUPPORTED_DATA_TYPES]:
    if experience_path is None:
        experience_path = get_experience_directory()

    if experience_path.is_dir():
        return get_experience_from_folder(experience_path)

    return [get_experience_from_file(experience_path)]


def get_experience_from_folder(experience_path: Path) -> list[SUPPORTED_DATA_TYPES]:
    list_of_experience = []
    for file_path in experience_path.iterdir():
        if file_path.suffix != ".yaml":
            continue

        if (
            _is_template_files_ignored(experience_path)
            and file_path.name in TEMPLATE_FILES_TO_IGNORE
        ):
            continue

        experience = get_experience_from_file(file_path)
        list_of_experience.append(experience)

    return list_of_experience


def get_experience_from_file(file_path: Path) -> SUPPORTED_DATA_TYPES:
    if file_path.suffix != ".yaml":
        raise ValueError("Only .yaml files are supported")

    with open(file_path, "r") as file:
        data = yaml.safe_load(file)
        for data_type in EXPERIENCE_DATA_TYPES:
            validated_data = get_pydantic_data_from_dict(data, data_type)
            if validated_data is None:
                continue

            return validated_data

    raise ValueError(
        f"File data does not match any known data types\n File Name: {file_path}"
    )


def get_pydantic_data_from_dict(
    data: dict, data_type: type[BaseModel]
) -> BaseModel | None:
    try:
        return data_type.model_validate(data)
    except Exception:
        return None


def _is_template_files_ignored(
    experience_path: Path,
) -> bool:
    return len(list(experience_path.glob("*.yaml"))) > len(TEMPLATE_FILES_TO_IGNORE)
