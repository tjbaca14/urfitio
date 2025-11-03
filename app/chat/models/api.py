from datetime import datetime
from typing import List

from pydantic import BaseModel

from app.common.models import Message


class ChatRequest(BaseModel):
    id: str
    userId: str
    contextQuery: dict[str, str] | None = None
    messages: List[Message]
    metadata: dict | None = None
    createdDate: datetime | None = None


class ChatResponse(BaseModel):
    """
    API response model for chat endpoint.
    Returns the assistant's message.
    """

    role: str
    content: str

    @classmethod
    def from_message(cls, message: Message) -> "ChatResponse":
        """Create ChatResponse from Message."""
        return cls(role=message.role, content=message.content)
