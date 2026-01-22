"""Chat domain dependencies."""

from fastapi import Depends

from app.chat.repository import ChatRepository
from app.chat.services.chat_application import ChatApplicationService
from app.chat.services.conversation_store import ConversationStore
from app.rag.dependencies import get_rag_pipeline
from app.rag.pipeline import RAGPipeline


async def get_chat_repository() -> ChatRepository:
    """Get ChatRepository instance."""
    return ChatRepository()


async def get_conversation_store(
    repository: ChatRepository = Depends(get_chat_repository),
) -> ConversationStore:
    """
    Get ConversationStore with repository.

    Args:
        repository: Chat repository for data access

    Returns:
        ConversationStore instance
    """
    return ConversationStore(repository)


async def get_chat_application_service(
    rag_pipeline: RAGPipeline = Depends(get_rag_pipeline),
    conversation_store: ConversationStore = Depends(get_conversation_store),
) -> ChatApplicationService:
    """
    Get ChatApplicationService with all dependencies.

    Chat domain consumes RAG pipeline from rag domain.

    Args:
        rag_pipeline: Configured RAG pipeline (from rag domain)
        conversation_store: Conversation persistence service

    Returns:
        ChatApplicationService instance
    """
    return ChatApplicationService(rag_pipeline, conversation_store)
