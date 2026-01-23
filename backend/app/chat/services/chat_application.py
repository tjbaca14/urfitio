"""Chat service - business logic for school recruiting chat."""

from datetime import datetime
from typing import List, Optional

import pytz
from app.chat.models.dto import ChatHistoryDTO, ChatRequest
from app.chat.services.conversation_store import ConversationStore
from app.common.models import Message
from app.rag.pipeline import RAGPipeline
from app.utils import get_logger
from sqlalchemy.ext.asyncio import AsyncSession

logger = get_logger(__name__)


class ChatApplicationService:
    """
    School recruiting chat service.

    Orchestrates the complete chat feature:
    1. RAG pipeline for context-aware responses
    2. Conversation persistence
    3. Chat history management

    This is the business domain service for school chat functionality.
    """

    def __init__(
        self,
        rag_pipeline: RAGPipeline,
        conversation_store: ConversationStore,
    ):
        """
        Initialize chat service.

        Args:
            rag_pipeline: RAG pipeline for generating context-aware responses
            conversation_store: Service for persisting conversations
        """
        self.rag_pipeline = rag_pipeline
        self.conversation_store = conversation_store

    async def generate_response(
        self,
        chat_request: ChatRequest,
    ) -> Message:
        """
        Generate a chat response using RAG.

        Flow:
        1. Retrieve context based on contextKey (if provided)
        2. Augment messages with context
        3. Call LLM to generate response
        4. Return assistant's message

        Args:
            chat_request: Chat request with messages and optional context query

        Returns:
            Assistant's response message
        """
        logger.info(f"Generating response for chat: {chat_request.id}")

        response_message = await self.rag_pipeline.run(
            messages=chat_request.messages,
            context_key=chat_request.context_key,
        )

        logger.info(f"Response generated for chat: {chat_request.id}")
        return response_message

    async def save_conversation(
        self,
        session: AsyncSession,
        chat_request: ChatRequest,
    ) -> ChatHistoryDTO:
        """
        Save or update a conversation.

        Converts domain ChatRequest to infrastructure ChatHistoryDTO,
        then persists using ConversationStore.

        Args:
            session: Database session
            chat_request: Chat request to save

        Returns:
            Saved chat history
        """
        logger.info(f"Saving conversation: {chat_request.id}")

        # Convert domain model (ChatRequest) to infrastructure DTO (ChatHistoryDTO)
        chat_history_dto = self._to_chat_history_dto(chat_request)

        # Persist using infrastructure service
        return await self.conversation_store.save_conversation(
            session, chat_history_dto
        )

    async def get_conversation(
        self,
        session: AsyncSession,
        chat_id: str,
    ) -> Optional[ChatHistoryDTO]:
        """
        Get conversation by ID.

        Args:
            session: Database session
            chat_id: Chat identifier

        Returns:
            Chat history or None if not found
        """
        return await self.conversation_store.get_conversation(session, chat_id)

    async def get_user_conversations(
        self,
        session: AsyncSession,
        user_id: str,
        limit: int = 10,
        offset: int = 0,
    ) -> List[ChatHistoryDTO]:
        """
        Get all conversations for a user.

        Args:
            session: Database session
            user_id: User identifier
            limit: Maximum number of conversations to return
            offset: Number of records to skip

        Returns:
            List of chat histories
        """
        return await self.conversation_store.get_user_conversations(
            session, user_id, limit=limit, offset=offset
        )

    def _to_chat_history_dto(self, chat_request: ChatRequest) -> ChatHistoryDTO:
        """
        Convert ChatRequest (domain) to ChatHistoryDTO (infrastructure).

        This conversion happens in the domain layer, not in infrastructure.

        Args:
            chat_request: Domain chat request

        Returns:
            Infrastructure DTO for persistence
        """
        # Convert Message objects to dicts
        messages = [message.model_dump() for message in chat_request.messages]

        # Use provided created_date or current time
        created_date = chat_request.created_date or datetime.now(
            pytz.timezone("America/Los_Angeles")
        )
        updated_date = datetime.now(pytz.timezone("America/Los_Angeles"))

        return ChatHistoryDTO(
            id=chat_request.id,
            user_id=chat_request.user_id,
            messages=messages,
            created_date=created_date,
            updated_date=updated_date,
        )
