from typing import Dict, Optional

from app.utils import get_logger

logger = get_logger(__name__)


class ContextRetriever:
    """
    Generic context retriever for RAG systems.
    Retrieves context from a flat cache based on a string query.

    This is a generic component - no application-specific logic.
    """

    def __init__(self, cache: Dict[str, str]):
        """
        Initialize context retriever.

        Args:
            cache: Flat cache mapping keys to context strings
            generic_context: Default context when no specific key is provided
        """
        self.cache = cache

    async def retrieve(self, query: str) -> Optional[str]:
        """
        Retrieve context based on a query string.

        Args:
            query: String key to look up in cache (e.g., school name)

        Returns:
            Context string from cache, or generic context if not found
        """

        context = self.cache.get(query, None)
        return context
