from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class ChatHistoryDTO(BaseModel):
    """DTO for ChatHistory entity"""

    model_config = ConfigDict(from_attributes=True)

    id: str
    user_id: str
    messages: List[dict]
    created_date: datetime
    updated_date: Optional[datetime] = None


class ChatHistoryCreateDTO(BaseModel):
    """DTO for creating chat history"""

    id: str
    user_id: str
    messages: List[dict]
    created_date: datetime


class ChatHistoryUpdateDTO(BaseModel):
    """DTO for updating chat history"""

    messages: Optional[List[dict]] = None
    updated_date: Optional[datetime] = None


class FeedbackDTO(BaseModel):
    """DTO for Feedback entity"""

    model_config = ConfigDict(from_attributes=True)

    id: str
    user_id: str
    feedback: str
    category: Optional[str] = None
    created_date: datetime


class FeedbackCreateDTO(BaseModel):
    """DTO for creating feedback"""

    id: str
    user_id: str
    feedback: str
    category: Optional[str] = None
    created_date: datetime
