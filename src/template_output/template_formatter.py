import jinja2
from pydantic import BaseModel
from .template_loader import Template, TemplateTypes, OutputFormatTypes


def get_formatted_output(
    template: Template,
    required_fields: BaseModel,
) -> str:

    env = jinja2.Environment()
    if template.output_format_type == OutputFormatTypes.LATEX:
        env = jinja2.Environment(
            block_start_string="<%",
            block_end_string="%>",
            variable_start_string="<<",
            variable_end_string=">>",
            comment_start_string="<#",
            comment_end_string="#>",
        )
    jinja_template: jinja2.Template = env.from_string(template.template_content)

    jinja_variables = _get_formatted_dict_for_jinja(required_fields)
    if template.output_format_type == OutputFormatTypes.LATEX:
        jinja_variables = _escape_all_strings_latex(jinja_variables)

    rendered_content = jinja_template.render(jinja_variables)

    return rendered_content


def _get_formatted_dict_for_jinja(
    required_fields: BaseModel,
) -> dict:
    return required_fields.model_dump()


def _escape_all_strings_latex(
    object_to_escape: dict | list | str,
) -> dict | list | str:

    if isinstance(object_to_escape, str):
        return _get_string_to_latex_escaped(object_to_escape)
    elif isinstance(object_to_escape, list):
        latex_ready_list = []
        for i in range(len(object_to_escape)):
            latex_ready_item = _escape_all_strings_latex(object_to_escape[i])
            latex_ready_list.append(latex_ready_item)
        return latex_ready_list
    elif isinstance(object_to_escape, dict):
        latex_ready_dict = {}
        for key, value in object_to_escape.items():
            latex_ready_value = _escape_all_strings_latex(value)
            latex_ready_dict[key] = latex_ready_value
        return latex_ready_dict

    return object_to_escape


def _get_string_to_latex_escaped(input_string: str) -> str:
    return (
        input_string.replace("\\", "\\\\")
        .replace("#", "\\#")
        .replace("$", "\\$")
        .replace("%", "\\%")
        .replace("&", "\\&")
        .replace("~", "\\~")
        .replace("_", "\\_")
        .replace("^", "\\^")
        .replace("{", "\\{")
        .replace("}", "\\}")
    )
