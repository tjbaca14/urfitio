from typing import List

from pydantic import BaseModel

from app.common.models import Message


class LLMRequest(BaseModel):
    """
    Generic LLM request model.

    Used internally by LLM providers to structure API requests.
    """

    model: str
    max_tokens: int
    system: str
    messages: List[Message]
    temperature: float
