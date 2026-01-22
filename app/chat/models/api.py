from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from app.common.models import Message


class ChatRequest(BaseModel):
    id: str
    userId: str
    contextQuery: Optional[str] = None
    messages: List[Message]
    metadata: dict | None = None
    createdDate: datetime | None = None


class ChatResponse(ChatRequest):
    pass
