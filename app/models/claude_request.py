from typing import List

from pydantic import BaseModel

from app.models.chat import Message


class ClaudeRequest(BaseModel):
    model: str
    max_tokens: int
    system: str
    messages: List[Message]