from enum import Enum
from pydantic import Field, create_model, BaseModel
from typing import get_origin, get_args
import os

from .open_router_facade import (
    get_structured_llm_response as open_router_get_structured_llm_response,
)


class SourceEnum(str, Enum):
    OPEN_ROUTER = "open_router"


def get_structured_llm_response(
    prompt: str,
    output_format: type[BaseModel],
    model: str = None,
    source: SourceEnum = SourceEnum.OPEN_ROUTER,
    debug_questions: list[str] = None,
) -> BaseModel:
    if _is_debug_mode():
        prompt, output_format = _debug_mode_preprocessing(
            prompt, output_format, debug_questions
        )

    formatted_response = None
    if source == SourceEnum.OPEN_ROUTER:
        formatted_response = open_router_get_structured_llm_response(
            prompt=prompt,
            output_format=output_format,
            model=model,
        )
    else:
        raise ValueError(
            f"Unsupported LLM source: {source}, Create another llm facade and add it as an option."
        )

    if _is_debug_mode():
        _debug_mode_postprocessing(prompt, formatted_response)

    return formatted_response


# region LLM Debugging tools


def _debug_mode_preprocessing(prompt, output_format, debug_questions):
    prompt = _get_debuggable_prompt(prompt, debug_questions)
    output_format = _get_debuggable_format_recursive(output_format)
    return prompt, output_format


def _debug_mode_postprocessing(prompt, formatted_response):
    with open("/tmp/debug_response.md", "w") as f:
        json_format = formatted_response.model_dump_json(indent=2)
        f.write(
            f"# Response JSON\n\n```json\n{json_format}\n```\n # Prompt \n\n```text\n{prompt}\n```"
        )


def _get_debuggable_prompt(prompt, debug_questions):
    prompt = f"""{prompt}
        # DEBUG MODE
        You are in DEBUG MODE. 
        You will now explain your reasoning for each field you fill in the output format.
        You will go into detail about which exact lines from the prompt that led you to fill in each field.
        You will let the user see your work so they can understand your thought process.
        You will let the user know if there are any contradictions or ambiguities in the prompt that made it hard to fill in certain fields.
        """
    if isinstance(debug_questions, list):
        prompt += f"""            
        ## Debug Questions
        {'\n -'.join(debug_questions)}
        """

    return prompt


def _get_debuggable_format_recursive(
    output_format: type[BaseModel], depth=0
) -> type[BaseModel]:
    original_fields = {}
    list_of_fields = output_format.model_fields.items()
    for (
        field_name,
        field_info,
    ) in list_of_fields:
        field_type = field_info.annotation
        debug_field_type = str
        debug_description = "Display the exact lines from the prompt that led you to fill in value for the matching non debug field. Use direct quotes from the prompt to show your work clearly. Where its first quote: '<quote from prompt>' then explenation of value: '<explanation>'."

        # Handle any nested classes recursively
        if isinstance(field_type, type) and issubclass(field_type, BaseModel):
            field_type = _get_debuggable_format_recursive(field_type, depth=depth + 1)

        # Handle and base generic types like list as it is not a class or an instance
        elif get_origin(field_type) is list:
            item_type = get_args(field_type)[0]
            if isinstance(item_type, type) and issubclass(item_type, BaseModel):
                debug_item_type = _get_debuggable_format_recursive(
                    item_type, depth=depth + 1
                )
                field_type = list[debug_item_type]
            else:
                debug_field_type = list[str]
                debug_description = "For each item in the list, display the exact lines from the prompt that led you to fill in value for the matching non debug field. Use direct quotes from the prompt to show your work clearly. Where its first quote: '<quote from prompt>' then explenation of value: '<explanation>'."

        # Handle dict generic type like the list case
        elif get_origin(field_type) is dict:
            key_type, value_type = get_args(field_type)
            if isinstance(value_type, type) and issubclass(value_type, BaseModel):
                debug_value_type = _get_debuggable_format_recursive(
                    value_type, depth=depth + 1
                )
                field_type = dict[key_type, debug_value_type]
            else:
                debug_field_type = dict[key_type, str]
                debug_description = "For each key-value pair in the dictionary, display the exact lines from the prompt that led you to fill in value for the matching non debug field. Use direct quotes from the prompt to show your work clearly. Where its first quote: '<quote from prompt>' then explenation of value: '<explanation>'."

        original_fields[field_name] = (field_type, field_info)
        original_fields[f"{field_name}_debug"] = (
            debug_field_type,
            Field(
                description=debug_description,
            ),
        )

    if depth == 0:
        original_fields["debug_question_responses"] = (
            list[str],
            Field(
                description="For each question in the debug question responses answer them fully and in detail here. Use direct quotes from the prompt to show your work clearly. Where its first quote: '<quote from prompt>' then explenation of value: '<explanation>'.",
            ),
        )

    return create_model(f"{output_format.__name__}WithDebug", **original_fields)


def _is_debug_mode() -> bool:
    return os.getenv("LLM_DEBUG_MODE", "false").lower() == "true"


# endregion
