import pytest
from pydantic import BaseModel, Field
from src.llm.open_router_facade import get_structured_llm_response


def test_get_llm_response_returns_a_valid_response():
    response = get_structured_llm_response(
        "Give me a very short response in the format. Any values will do",
        _DummyResponseModel,
    )

    assert isinstance(response, _DummyResponseModel)


class _DummyResponseModel(BaseModel):
    message: str = Field(description="A very short message from the LLM")
    list_of_numbers: list[int] = Field(description="A very short list of integers")
