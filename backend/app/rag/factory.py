"""Factory for creating RAG pipeline instances."""

from app.integrations.llm import BaseLLMProvider
from app.rag.pipeline import RAGPipeline, Retriever
from app.rag.prompt_builder import PromptBuilder


def create_rag_pipeline(
    retriever: Retriever,
    llm_provider: BaseLLMProvider,
) -> RAGPipeline:
    """
    Factory function to create a configured RAG pipeline.

    Args:
        retriever: Context retriever implementation (domain-agnostic)
        llm_provider: LLM provider instance (Anthropic, OpenAI, etc.)

    Returns:
        Configured RAGPipeline instance
    """
    return RAGPipeline(
        context_retriever=retriever,
        prompt_builder=PromptBuilder(),
        llm_provider=llm_provider,
    )
