"""Chat domain dependencies."""

from app.adapters.rag.default_prompt_builder import DefaultPromptBuilder
from app.adapters.rag.school_retriever import SchoolContextRetriever
from app.adapters.rag.simple_generator import SimpleGenerator
from app.chat.repository import ChatRepository
from app.chat.services.chat_orchestration import ChatOrchestrationService
from app.chat.services.chat_persistence import ChatPersistenceService
from app.integrations.llm.base import LLMProvider
from app.ncaa.schools.dependencies import get_school_cache_service
from app.ncaa.schools.service.cache_service import SchoolCacheService
from app.rag.factory import create_rag_pipeline
from app.rag.pipeline import Generator, PromptBuilder, RAGPipeline, Retriever
from app.settings import LLMConfig
from fastapi import Depends, Request


async def get_llm_config(request: Request) -> LLMConfig:
    return request.app.state.llm_config


async def get_llm_provider(request: Request) -> LLMProvider:
    """Get LLM provider instance (Anthropic, OpenAI, etc.)."""
    return request.app.state.llm_provider


async def get_retriever(
    school_cache_service: SchoolCacheService = Depends(get_school_cache_service),
) -> Retriever:
    return SchoolContextRetriever(school_cache_service)


async def get_generator(
    llm_provider: LLMProvider = Depends(get_llm_provider),
) -> Generator:
    return SimpleGenerator(llm_provider)


async def get_prompt_builder() -> PromptBuilder:
    return DefaultPromptBuilder()


async def get_rag_pipeline(
    retriever: Retriever = Depends(get_retriever),
    prompt_builder: PromptBuilder = Depends(get_prompt_builder),
    generator: Generator = Depends(get_generator),
) -> RAGPipeline:
    """
    Get fully configured RAG pipeline.

    Assembles RAG pipeline with all dependencies (retriever, prompt builder, LLM).

    Args:
        retriever: Context retriever implementation
        prompt_builder: Prompt builder implementation
        llm_provider: Generator implementation from app state

    Returns:
        Configured RAGPipeline instance
    """
    return create_rag_pipeline(retriever, prompt_builder, generator)


async def get_chat_repository() -> ChatRepository:
    """Get ChatRepository instance."""
    return ChatRepository()


async def get_chat_persistence_service(
    repository: ChatRepository = Depends(get_chat_repository),
) -> ChatPersistenceService:
    """
    Get ChatPersistenceService with repository.

    Args:
        repository: Chat repository for data access

    Returns:
        ChatPersistenceService instance
    """
    return ChatPersistenceService(repository)


async def get_chat_orchestration_service(
    rag_pipeline: RAGPipeline = Depends(get_rag_pipeline),
    chat_persistence_service: ChatPersistenceService = Depends(get_chat_persistence_service),
) -> ChatOrchestrationService:
    """
    Get ChatOrchestrationService with all dependencies.

    Chat domain consumes RAG pipeline from rag domain.

    Args:
        rag_pipeline: Configured RAG pipeline (from rag domain)
        chat_persistence_service: Conversation persistence service

    Returns:
        ChatOrchestrationService instance
    """
    return ChatOrchestrationService(rag_pipeline, chat_persistence_service)
