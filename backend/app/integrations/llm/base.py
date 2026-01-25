from typing import List, Protocol

from app.common.models import Message


class LLMProvider(Protocol):
    """
    Abstract base class for all LLM providers.

    Defines the contract that all LLM provider implementations must follow.
    Providers are responsible for:
    - Translating universal Message format to provider-specific format
    - Making HTTP requests to provider APIs
    - Translating provider responses back to universal Message format
    """

    async def invoke(
        self,
        messages: List[Message],
        temperature: float = 0.7,
        max_tokens: int = 1024,
    ) -> Message:
        """
        Generate a response from the LLM provider.

        Args:
            messages: Conversation messages in universal format.
                     May include system messages (role="system") which
                     providers should handle appropriately.
            temperature: Sampling temperature (0.0 to 1.0)
            max_tokens: Maximum tokens to generate

        Returns:
            Assistant message with generated response

        Raises:
            HTTPException: On API errors, network issues, or unexpected failures
        """
        ...
