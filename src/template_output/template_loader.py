from enum import Enum
import importlib
from pathlib import Path
from pydantic import BaseModel


class OutputFormatTypes(Enum):
    LATEX = "tex"


class TemplateTypes(Enum):
    COVER_LETTER = "cover_letter"
    RESUME = "resume"


class Template(BaseModel):
    template_path: Path
    required_fields: type[BaseModel]
    template_content: str
    output_format_type: OutputFormatTypes
    template_type: TemplateTypes


def get_resume_template(format_folder_path: Path) -> Template:
    template_path = _get_required_file_from_template_folder(
        format_folder_path, "template.*"
    )
    template_type = OutputFormatTypes(template_path.suffix.lstrip("."))
    template_content = _load_template_content(template_path)

    required_fields_path = _get_required_file_from_template_folder(
        format_folder_path, "required_fields.py"
    )
    required_fields = _load_expected_output_format(required_fields_path)

    return Template(
        template_path=template_path,
        required_fields=required_fields,
        template_content=template_content,
        output_format_type=template_type,
        template_type=TemplateTypes.RESUME,
    )


def get_cover_letter_template(format_folder_path: Path) -> Template:
    template_path = _get_required_file_from_template_folder(
        format_folder_path, "cover_letter_template.*"
    )
    template_type = OutputFormatTypes(template_path.suffix.lstrip("."))
    template_content = _load_template_content(template_path)

    required_fields_path = _get_required_file_from_template_folder(
        format_folder_path, "cover_letter_required_fields.py"
    )
    required_fields = _load_expected_output_format(required_fields_path)

    return Template(
        template_path=template_path,
        required_fields=required_fields,
        template_content=template_content,
        output_format_type=template_type,
        template_type=TemplateTypes.COVER_LETTER,
    )


def _get_required_file_from_template_folder(
    format_folder_path: Path, file_name_regex: str
) -> Path:
    if not format_folder_path.is_dir():
        raise NotADirectoryError(
            f"The template path provided is not a directory: {format_folder_path}"
        )

    template_files = list(format_folder_path.glob(file_name_regex))
    if not template_files:
        raise FileNotFoundError(
            f"The file that is required to be named 'templateNo' is not found in the given template directory provided: {format_folder_path}"
        )

    return template_files[0]


def _load_template_content(template_format_path: Path) -> str:

    if not template_format_path.exists():
        raise FileNotFoundError(
            f"Template file is not found with name template.tex. The folder we looked at is: {template_format_path}"
        )

    with open(template_format_path, "r") as f:
        template_content = f.read()

    return template_content


def _load_expected_output_format(required_fields_path: Path) -> type[BaseModel]:
    CLASS_NAME = "RequiredFields"

    spec = importlib.util.spec_from_file_location(
        "required_fields", required_fields_path
    )
    required_fields_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(required_fields_module)  # type: ignore

    if not hasattr(required_fields_module, CLASS_NAME):
        raise AttributeError(
            f"The module at {required_fields_path} does not have a class named {CLASS_NAME}"
        )

    return required_fields_module.RequiredFields
