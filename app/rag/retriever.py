from typing import Any, Dict, Optional

from app.utils import get_logger

logger = get_logger(__name__)


class ContextRetriever:
    """
    Generic context retriever for RAG systems.
    Retrieves context from any hierarchical data source based on a query.

    This is a generic component - no application-specific logic.
    """

    def __init__(self, data_source: Dict[str, Any]):
        """
        Initialize context retriever.

        Args:
            data_source: Hierarchical data structure (nested dicts)
        """
        self.data_source = data_source

    def retrieve(self, query: Optional[Dict[str, str]]) -> Optional[str]:
        """
        Retrieve context based on a query dictionary.

        Args:
            query: Dictionary containing keys to navigate data structure
                   e.g., {"level1": "value1", "level2": "value2"}

        Returns:
            Context string or None if not found
        """
        if not query:
            logger.debug("No query provided")
            return None

        try:
            # Navigate the data structure using query keys
            current = self.data_source
            path = []

            for key, value in query.items():
                if not isinstance(current, dict):
                    logger.warning(
                        f"Expected dict at {'.'.join(path)}, got {type(current)}"
                    )
                    return None

                current = current.get(value)
                path.append(f"{key}={value}")

                if current is None:
                    logger.warning(f"Path not found: {'.'.join(path)}")
                    return None

            # Return the final value as string
            if isinstance(current, str):
                logger.info(f"Context retrieved: {'.'.join(path)}")
                return current
            else:
                logger.warning(
                    f"Expected string at {'.'.join(path)}, got {type(current)}"
                )
                return str(current) if current else None

        except Exception as e:
            logger.error(f"Error retrieving context: {e}", exc_info=True)
            return None

    def has_context(self, query: Dict[str, str]) -> bool:
        """
        Check if context exists for given query.

        Args:
            query: Query dictionary

        Returns:
            True if context exists
        """
        return self.retrieve(query) is not None
