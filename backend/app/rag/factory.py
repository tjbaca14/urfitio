"""Factory for creating RAG pipeline instances."""

from app.integrations.llm import BaseLLMProvider
from app.rag.pipeline import PromptBuilder, RAGPipeline, Retriever


def create_rag_pipeline(
    retriever: Retriever,
    prompt_builder: PromptBuilder,
    llm_provider: BaseLLMProvider,
) -> RAGPipeline:
    """
    Factory function to create a configured RAG pipeline.

    Args:
        retriever: Context retriever implementation (domain-agnostic)
        prompt_builder: Prompt builder implementation (domain-agnostic)
        llm_provider: LLM provider instance (Anthropic, OpenAI, etc.)

    Returns:
        Configured RAGPipeline instance
    """
    return RAGPipeline(
        context_retriever=retriever,
        prompt_builder=prompt_builder,
        llm_provider=llm_provider,
    )
