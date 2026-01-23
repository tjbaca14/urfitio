from typing import List

from app.common.models import Message
from pydantic import BaseModel


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
