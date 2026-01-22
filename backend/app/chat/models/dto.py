"""Chat domain data transfer objects."""

from datetime import datetime
from typing import List, Optional

from pydantic import Field

from app.common.models import BaseDTOModel, Message


class ChatRequest(BaseDTOModel):
    """
    DTO for chat requests (API).

    Chat domain request model that accepts camelCase from frontend
    and converts to snake_case internally.
    """

    model_config = {"populate_by_name": True}

    id: str
    user_id: str = Field(..., alias="userId")
    context_key: Optional[str] = Field(None, alias="contextKey")
    messages: List[Message]
    metadata: Optional[dict] = None
    created_date: Optional[datetime] = Field(None, alias="createdDate")


class ChatHistoryDTO(BaseDTOModel):
    """
    DTO for ChatHistory entity (repository return type).

    Supports both camelCase (API) and snake_case (DB) via aliases.
    """

    model_config = {"populate_by_name": True}

    id: str
    user_id: str
    messages: List[dict]
    created_date: datetime
    updated_date: Optional[datetime] = None
