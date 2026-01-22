"""
School context retriever adapter.

Bridges the Schools domain and RAG domain without either knowing about each other.
"""

from typing import Optional

from app.schools.service.cache_service import SchoolCacheService
from app.utils import get_logger

logger = get_logger(__name__)


class SchoolContextRetriever:
    """
    Adapter that implements RAG's Retriever protocol using Schools domain services.

    This adapter allows the generic RAG pipeline to retrieve school-specific
    context without the RAG domain knowing about schools, and without the
    schools domain knowing about RAG.
    """

    def __init__(self, cache_service: SchoolCacheService):
        """
        Initialize school context retriever.

        Args:
            cache_service: School cache service for retrieving contexts
        """
        self._cache_service = cache_service

    async def retrieve(self, query: str) -> Optional[str]:
        """
        Retrieve school context based on school name query.

        Implements the Retriever protocol required by RAGPipeline.

        Args:
            query: School name to look up

        Returns:
            School context if found, None otherwise
        """
        context = await self._cache_service.get_school_context(query)

        if context:
            logger.info(f"Retrieved context for school: {query}")
        else:
            logger.warning(f"No context found for school: {query}")

        return context
