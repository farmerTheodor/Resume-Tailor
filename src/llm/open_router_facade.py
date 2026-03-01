import httpx
from pydantic import BaseModel

import os


DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "google/gemini-3-flash-preview")


def get_structured_llm_response(
    prompt: str, output_format: type[BaseModel], model: str = None
) -> BaseModel:
    if model is None:
        model = DEFAULT_MODEL

    headers = _get_headers()
    json_data = _get_json_data(prompt, output_format, model)

    response = httpx.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=json_data,
        timeout=120.0,
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
    api_key = os.getenv("OPEN_ROUTER_API_KEY")
    if api_key is None:
        raise ValueError(
            "OPEN_ROUTER_API_KEY environment variable is not set. To use Open Router, please set this variable with your api key using the .env file."
        )

    return f"Bearer {api_key}"


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
    output_in_json_format = _get_response_json(response_input)

    return output_format.model_validate_json(output_in_json_format)


def _get_response_json(
    response_input: httpx.Response,
) -> dict:
    return response_input.json()["choices"][0]["message"]["content"]
