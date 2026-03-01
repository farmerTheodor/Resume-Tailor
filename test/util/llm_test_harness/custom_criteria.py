from pydantic import BaseModel, Field
from .open_router_facade import get_structured_llm_response


class CustomCriteria(BaseModel):
    score: int = Field(
        description="""A Score between 1-5 indicating how good the response satisfies the assertion.
        - 1 means the response does not satisfy the assertion at all.
        - 2 means the response barely satisfies the assertion.
        - 3 means the response somewhat satisfies the assertion.
        - 4 means the response mostly satisfies the assertion.
        - 5 means the response fully satisfies the assertion.
        """,
    )

    reason: str = Field(description="A concise explanation justifying the given score.")

    def __str__(self) -> str:
        return f"""
==========================================================
Score: {self.score}

Reason: 
{self.reason}
==========================================================
"""


def get_score_for_criteria(
    response_text: str, assertion_criteria: str
) -> CustomCriteria:
    prompt = DEFAULT_PROMPT.format(
        response_text=response_text, assertion_criteria=assertion_criteria
    )

    return get_structured_llm_response(
        prompt=prompt,
        output_format=CustomCriteria,
    )


DEFAULT_PROMPT = """
You are an expert evaluator. Given a response and an assertion criteria, provide a score from 1 to 5 indicating how well the response satisfies the assertion criteria.
Evaluate the response based on the following criteria between "<<<Assertion Criteria" and ">>>":
<<<Assertion Criteria 
{assertion_criteria}
>>>

The response to evaluate is given between "<<<Response" and ">>>":
<<<Response
{response_text}
>>> 

Based on the above assertion criteria, provide your evaluation in the following JSON format:
"""
