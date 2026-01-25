"""Cache client abstraction and implementations."""

import pickle
from enum import StrEnum
from typing import Any, Dict, Optional, Protocol


class CacheClient(Protocol):
    """
    Abstract cache storage client.

    Defines interface for cache operations that can be implemented
    with different backends (in-memory, Redis, Memcached, etc.).

    All implementations handle serialization internally.
    """

    async def get(self, key: str) -> Optional[Any]:
        """
        Get value by key.

        Args:
            key: Cache key

        Returns:
            Deserialized value if exists, None otherwise
        """
        ...

    async def set(self, key: str, value: Any) -> None:
        """
        Set key-value pair.

        Args:
            key: Cache key
            value: Value to store (will be serialized internally)
        """
        ...

    async def set_many(self, items: Dict[str, Any]) -> None:
        """
        Set multiple key-value pairs.

        Args:
            items: Dict of key-value pairs to store (will be serialized internally)
        """
        ...

    async def clear(self) -> None:
        """Clear all cache entries."""
        ...


class InMemoryCacheClient:
    """
    In-memory cache implementation.

    Stores data as pickled bytes in memory for consistency with remote cache
    implementations and to prevent reference mutations.

    Not suitable for distributed systems or persistence across restarts.
    """

    def __init__(self):
        """Initialize empty in-memory cache."""
        self._cache: Dict[str, bytes] = {}

    async def get(self, key: str) -> Optional[Any]:
        """
        Get value by key from in-memory cache.

        Deserializes the stored bytes back to Python object.
        """
        data = self._cache.get(key)
        return pickle.loads(data) if data else None

    async def set(self, key: str, value: Any) -> None:
        """
        Set key-value pair in in-memory cache.

        Serializes the value to bytes before storing.
        """
        self._cache[key] = pickle.dumps(value)

    async def get_all(self) -> Dict[str, Any]:
        """
        Get all key-value pairs from in-memory cache.

        Deserializes all stored values.
        """
        return {key: pickle.loads(data) for key, data in self._cache.items()}

    async def set_many(self, items: Dict[str, Any]) -> None:
        """
        Set multiple key-value pairs in in-memory cache.

        Serializes all values to bytes before storing.
        """
        for key, value in items.items():
            self._cache[key] = pickle.dumps(value)

    async def clear(self) -> None:
        """Clear all entries from in-memory cache."""
        self._cache.clear()


class CacheClientType(StrEnum):
    IN_MEMORY = "IN_MEMORY"
    REDIS = "REDIS"


def create_cache_client(cache_client_type: CacheClientType) -> CacheClient:
    if cache_client_type == CacheClientType.IN_MEMORY:
        return InMemoryCacheClient()
    else:
        raise ValueError(
            f"Invalid cache_client_type: {cache_client_type}. Must be one of [{CacheClientType}]."
        )
