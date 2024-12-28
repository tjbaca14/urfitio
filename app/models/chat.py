from typing import List

from pydantic import BaseModel


class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    id: str
    contextKey: str
    messages: List[Message]
    metadata: dict | None = None
