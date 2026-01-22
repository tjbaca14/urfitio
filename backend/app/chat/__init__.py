"""Chat domain - school recruiting chat feature."""

from app.common.models import Message

from .models.dto import ChatRequest
from .routes import chat_router
from .services.chat_application import ChatApplicationService

__all__ = [
    "ChatRequest",
    "Message",
    "chat_router",
    "ChatApplicationService",
]
