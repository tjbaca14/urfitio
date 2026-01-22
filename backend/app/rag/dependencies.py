"""RAG domain dependencies."""

from fastapi import Depends

from app.common.dependencies import get_llm_provider
from app.integrations.llm import BaseLLMProvider
from app.ncaa.schools.dependencies import get_school_cache_service
from app.ncaa.schools.service.cache_service import SchoolCacheService
from app.rag.factory import create_rag_pipeline
from app.rag.pipeline import PromptBuilder, RAGPipeline, Retriever
from app.rag.prompt_builders import DefaultPromptBuilder
from app.rag.retrievers import SchoolContextRetriever


async def get_retriever(
    school_cache_service: SchoolCacheService = Depends(get_school_cache_service),
) -> Retriever:
    """
    Get context retriever implementation.

    Wires up the concrete SchoolContextRetriever to the generic Retriever protocol.

    Args:
        school_cache_service: School cache service from app state

    Returns:
        Retriever implementation (SchoolContextRetriever)
    """
    return SchoolContextRetriever(school_cache_service)


async def get_prompt_builder() -> PromptBuilder:
    """
    Get prompt builder implementation.

    Returns:
        PromptBuilder implementation (DefaultPromptBuilder)
    """
    return DefaultPromptBuilder()


async def get_rag_pipeline(
    retriever: Retriever = Depends(get_retriever),
    prompt_builder: PromptBuilder = Depends(get_prompt_builder),
    llm_provider: BaseLLMProvider = Depends(get_llm_provider),
) -> RAGPipeline:
    """
    Get fully configured RAG pipeline.

    Assembles RAG pipeline with all dependencies (retriever, prompt builder, LLM).

    Args:
        retriever: Context retriever implementation
        prompt_builder: Prompt builder implementation
        llm_provider: LLM provider from app state

    Returns:
        Configured RAGPipeline instance
    """
    return create_rag_pipeline(retriever, prompt_builder, llm_provider)
