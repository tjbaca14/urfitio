from typing import Dict, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.chat.models.api import ChatRequest
from app.chat.repository import ChatRepository
from app.chat.services import ConversationService
from app.common.models import Message
from app.integrations.llm.base import BaseLLMProvider
from app.rag import PromptBuilder, RAGPipeline
from app.rag.retriever import ContextRetriever
from app.utils import get_logger

logger = get_logger(__name__)


class ChatOrchestrator:
    """
    Chat-specific orchestrator.

    Responsibilities:
    - Delegate RAG flow to generic RAGPipeline
    - Manage conversation persistence
    - Coordinate chat-specific operations

    The generic RAG logic (retrieve→augment→generate) is handled by RAGPipeline.
    This orchestrator focuses on chat domain concerns like persistence.
    """

    def __init__(
        self,
        rag_pipeline: RAGPipeline,
        conversation_service: ConversationService,
    ):
        """
        Initialize chat orchestrator.

        Args:
            rag_pipeline: Generic RAG pipeline for generation
            conversation_service: Service for conversation persistence
        """
        self.rag_pipeline = rag_pipeline
        self.conversation_service = conversation_service

    async def process_chat(self, chat_request: ChatRequest) -> Message:
        """
        Process a chat request using generic RAG pipeline.

        Delegates the retrieve→augment→generate flow to RAGPipeline.

        Args:
            chat_request: Chat request with messages and optional context query

        Returns:
            Assistant's response message
        """
        logger.info(f"Processing chat request: {chat_request.id}")

        # Delegate to generic RAG pipeline
        response = await self.rag_pipeline.generate(
            messages=chat_request.messages,
            context_query=chat_request.contextQuery,
        )

        logger.info(f"Response generated for chat {chat_request.id}")
        return response

    async def save_chat(self, session: AsyncSession, chat_request: ChatRequest) -> None:
        """
        Save a conversation to the database.

        Args:
            session: SQLAlchemy async session
            chat_request: Chat request to save
        """
        await self.conversation_service.save_conversation(session, chat_request)
        logger.info(f"Chat saved: {chat_request.id}")

    async def process_and_save_chat(
        self,
        session: AsyncSession,
        chat_request: ChatRequest,
    ) -> Message:
        """
        Process chat and save the conversation in one operation.

        Args:
            session: SQLAlchemy async session
            chat_request: Chat request

        Returns:
            Assistant's response message
        """
        # Generate response
        response = await self.process_chat(chat_request)

        # Append response to messages
        chat_request.messages.append(response)

        # Save conversation
        await self.save_chat(session, chat_request)

        return response

    async def get_chat_history(
        self, session: AsyncSession, chat_id: str
    ) -> Optional[ChatRequest]:
        """
        Get chat history by ID.

        Args:
            session: SQLAlchemy async session
            chat_id: Chat identifier

        Returns:
            ChatRequest or None
        """
        chat_dto = await self.conversation_service.get_conversation(session, chat_id)

        if not chat_dto:
            return None

        # Convert DTO to ChatRequest
        messages = [Message(**msg) for msg in chat_dto.messages]
        return ChatRequest(
            id=chat_dto.id,
            userId=chat_dto.user_id,
            messages=messages,
            createdDate=chat_dto.created_date,
        )

    async def get_user_chat_history(
        self, session: AsyncSession, user_id: str, limit: int = 10
    ) -> list[ChatRequest]:
        """
        Get all chat history for a user.

        Args:
            session: SQLAlchemy async session
            user_id: User's UUID
            limit: Maximum number of chats to return

        Returns:
            List of ChatRequest objects
        """
        chat_dtos = await self.conversation_service.get_user_conversations(
            session, user_id, limit=limit
        )

        # Convert DTOs to ChatRequests
        chats = []
        for dto in chat_dtos:
            messages = [Message(**msg) for msg in dto.messages]
            chats.append(
                ChatRequest(
                    id=dto.id,
                    userId=dto.user_id,
                    messages=messages,
                    createdDate=dto.created_date,
                )
            )

        return chats


# Factory function for dependency injection
def create_chat_orchestrator(
    cache: Dict[str, Dict[str, str]], llm_provider: BaseLLMProvider
) -> ChatOrchestrator:
    """
    Factory function to create ChatOrchestrator with all dependencies.

    Creates:
    - CoachService (context provider)
    - RAGPipeline (generic retrieve→augment→generate with LLM)
    - ConversationService (chat persistence)
    - ChatOrchestrator (coordinates everything)

    Args:
        cache: Pre-loaded coach data cache
        llm_provider: LLM provider instance (Anthropic, OpenAI, etc.)

    Returns:
        Configured ChatOrchestrator instance
    """

    # Create coach service (implements ContextProvider)
    retriever = ContextRetriever(cache)

    # Create generic RAG pipeline with LLM provider
    rag_pipeline = RAGPipeline(
        context_retriever=retriever,
        prompt_builder=PromptBuilder(),
        llm_provider=llm_provider,
    )

    # Create conversation persistence service
    chat_repo = ChatRepository()
    conversation_service = ConversationService(chat_repo)

    # Create orchestrator with RAG pipeline
    return ChatOrchestrator(
        rag_pipeline=rag_pipeline,
        conversation_service=conversation_service,
    )
