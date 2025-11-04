from typing import List, Optional, Protocol

from app.common.models import Message
from app.integrations.llm import BaseLLMProvider
from app.rag.prompt_builder import PromptBuilder
from app.utils import get_logger

logger = get_logger(__name__)


class Retriever(Protocol):
    """
    Protocol for domain-specific context providers.

    Any domain that provides context for RAG must implement this interface.
    Examples: ContextRetriever, DocumentService, EmailContextService, etc.
    """

    async def retrieve(self, query: str) -> Optional[str]:
        """
        Retrieve context based on a query.

        Args:
            query: Domain-specific query parameters

        Returns:
            Context string to augment the prompt, or None if no context found
        """
        ...


class RAGPipeline:
    """
    Generic RAG (Retrieval-Augmented Generation) orchestrator.

    Composes and orchestrates:
    1. ContextProvider: Retrieves domain-specific context
    2. PromptBuilder: Augments messages with context and system prompts
    3. LLMProvider: Generates responses

    Implements the standard RAG flow:
    Retrieve → Augment → Generate

    This pipeline is domain-agnostic and reusable across any context provider.
    """

    def __init__(
        self,
        context_retriever: Retriever,
        prompt_builder: PromptBuilder,
        llm_provider: BaseLLMProvider,
    ):
        """
        Initialize RAG pipeline with all dependencies.

        Args:
            context_retriever: Domain-specific context provider (implements ContextProvider)
            prompt_builder: Prompt builder for augmentation and system prompts
            llm_provider: LLM provider for generation (Anthropic, OpenAI, etc.)
        """
        self.context_retriever = context_retriever
        self.prompt_builder = prompt_builder
        self.llm_provider = llm_provider

    async def generate(
        self,
        messages: List[Message],
        context_query: Optional[str] = None,
    ) -> Message:
        """
        Execute complete RAG pipeline: retrieve, augment, generate.

        Flow:
        1. Retrieve context from domain provider (if query provided)
        2. Augment last user message with context
        3. Ensure system prompt exists
        4. Generate response with LLM

        Args:
            messages: Conversation history
            context_query: Optional query for context retrieval

        Returns:
            Generated assistant message

        Raises:
            ValueError: If message list is empty or invalid
        """
        self._validate_messages(messages)

        context = await self._retrieve_context(context_query)
        augmented_messages = self._augment_messages(messages, context)
        final_messages = self._ensure_system_prompt(augmented_messages)

        response = await self.llm_provider.generate(messages=final_messages)
        logger.info("RAG pipeline completed successfully")
        return response

    def _validate_messages(self, messages: List[Message]) -> None:
        """Validate message list is not empty."""
        if not messages:
            raise ValueError("Cannot generate response with empty message list")

    async def _retrieve_context(self, context_query: Optional[str]) -> Optional[str]:
        """Retrieve context from domain provider."""
        if not context_query:
            logger.info("No context query provided, proceeding without context")
            return None

        context = await self.context_retriever.retrieve(context_query)

        return context

    def _augment_messages(
        self, messages: List[Message], context: Optional[str]
    ) -> List[Message]:
        """
        Augment last user message with context.

        Returns a copy with the last user message formatted with context.
        """
        # Copy to avoid mutation
        augmented = [Message(role=msg.role, content=msg.content) for msg in messages]

        last_message = augmented[-1]
        if last_message.role != "user":
            logger.warning(f"Last message is not from user: {last_message.role}")
            return augmented

        # Format with context using PromptBuilder
        formatted_content = self.prompt_builder.format_user_message(
            user_query=last_message.content,
            context=context,
        )
        augmented[-1].content = formatted_content
        logger.debug(f"User message augmented. Context present: {context is not None}")

        return augmented

    def _ensure_system_prompt(self, messages: List[Message]) -> List[Message]:
        """
        Ensure system prompt exists at the beginning of message list.

        In multi-turn conversations, system prompt may already exist.
        Only add if not present.
        """
        if messages[0].role == "system":
            return messages

        system_prompt = self.prompt_builder.get_system_prompt()
        return [Message(role="system", content=system_prompt)] + messages
