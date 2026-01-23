"""Factory for creating RAG pipeline instances."""

from app.rag.pipeline import Generator, PromptBuilder, RAGPipeline, Retriever


def create_rag_pipeline(
    retriever: Retriever,
    prompt_builder: PromptBuilder,
    llm_provider: Generator,
) -> RAGPipeline:
    """
    Factory function to create a configured RAG pipeline.

    Args:
        retriever: Context retriever implementation (domain-agnostic)
        prompt_builder: Prompt builder implementation (domain-agnostic)
        llm_provider: Generator implementation for LLM response generation

    Returns:
        Configured RAGPipeline instance
    """
    return RAGPipeline(
        context_retriever=retriever,
        prompt_builder=prompt_builder,
        llm_provider=llm_provider,
    )
