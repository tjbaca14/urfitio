"""Chat domain dependencies."""

from fastapi import Depends

from app.adapters.dependencies import get_retriever
from app.chat.repository import ChatRepository
from app.chat.services import ConversationService
from app.common.dependencies import get_llm_provider
from app.integrations.llm import BaseLLMProvider
from app.rag.factory import create_rag_pipeline
from app.rag.pipeline import RAGPipeline, Retriever


async def get_chat_repository() -> ChatRepository:
    """Get ChatRepository instance."""
    return ChatRepository()


async def get_conversation_service(
    repository: ChatRepository = Depends(get_chat_repository),
) -> ConversationService:
    """
    Get ConversationService with repository.

    Args:
        repository: Chat repository for data access

    Returns:
        ConversationService instance
    """
    return ConversationService(repository)


async def get_rag_pipeline(
    retriever: Retriever = Depends(get_retriever),
    llm_provider: BaseLLMProvider = Depends(get_llm_provider),
) -> RAGPipeline:
    """
    Get RAG pipeline with configured retriever and LLM.

    Chat domain depends on generic protocols (Retriever, BaseLLMProvider),
    not concrete implementations. The adapters layer provides the concrete retriever.

    Args:
        retriever: Generic context retriever (concrete impl from adapters)
        llm_provider: LLM provider from app state

    Returns:
        Configured RAGPipeline instance
    """
    return create_rag_pipeline(retriever, llm_provider)
