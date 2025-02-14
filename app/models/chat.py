from datetime import datetime
from typing import List

from pydantic import BaseModel


class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    id: str
    userId: str
    contextQuery: dict[str, str] | None = None
    messages: List[Message]
    metadata: dict | None = None
    createdDate: datetime | None = None
