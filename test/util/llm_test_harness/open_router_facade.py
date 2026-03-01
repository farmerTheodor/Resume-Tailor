import httpx
from pydantic import BaseModel
import os

DEFAULT_MODEL = "google/gemini-3-flash-preview"


def get_structured_llm_response(
    prompt: str, output_format: type[BaseModel], model: str = DEFAULT_MODEL
) -> BaseModel:
    headers = _get_headers()
    json_data = _get_json_data(prompt, output_format, model)

    response = httpx.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=json_data,
    )
    if response.status_code != 200:
        raise Exception(
            f"Open Router rejected the request with status code {response.status_code}: {response.text}"
        )

    return _get_response_in_output_format(response, output_format)


def _get_headers() -> dict[str, str]:
    return {
        "Authorization": _get_auth_header_value(),
        "Content-Type": "application/json",
    }


def _get_auth_header_value() -> str:
    return f"Bearer {os.getenv('OPEN_ROUTER_API_KEY')}"


def _get_json_data(
    prompt: str, output_format: type[BaseModel], model: str = DEFAULT_MODEL
) -> dict:
    return {
        "model": model,
        "reasoning": {"enabled": True},
        "messages": [
            {"role": "user", "content": prompt},
        ],
        "response_format": {
            "type": "json_schema",
            "json_schema": {
                "name": "response",
                "strict": True,
                "schema": output_format.model_json_schema(),
            },
        },
    }


def _get_response_in_output_format(
    response_input: httpx.Response, output_format: type[BaseModel]
) -> BaseModel:
    # Extract the content from the open router response
    output_in_json_format = response_input.json()["choices"][0]["message"]["content"]

    return output_format.model_validate_json(output_in_json_format)
