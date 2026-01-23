from typing import Any, List, Optional, Tuple

from app.common.clients.http_client import HTTPClient
from app.common.models import Message
from app.utils import get_logger

logger = get_logger(__name__)


class AnthropicProvider:
    """
    Anthropic Claude API provider implementation.

    Handles translation between universal Message format and Anthropic's
    API format, including system message extraction.
    """

    ANTHROPIC_VERSION = "2023-06-01"

    def __init__(
        self,
        api_key: str,
        model: str,
        base_url: str,
        http_client: HTTPClient,
    ):
        """
        Initialize Anthropic provider.

        Args:
            api_key: Anthropic API key
            model: Model name (e.g., "claude-3-sonnet-20240229")
            base_url: Anthropic API base URL
            http_client: HTTP client for making requests
        """
        self.api_key = api_key
        self.model = model
        self.base_url = base_url
        self.http_client = http_client

    async def generate(
        self,
        messages: List[Message],
        temperature: float = 0.7,
        max_tokens: int = 1024,
    ) -> Message:
        """
        Generate response from Anthropic Claude API.

        Args:
            messages: Conversation messages (may include system messages)
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate

        Returns:
            Assistant message with generated response
        """
        system_prompt, conversation = self._separate_system_messages(messages)

        anthropic_messages = self._to_anthropic_format(conversation)

        # Build request payload
        payload = {
            "model": self.model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": anthropic_messages,
        }

        # Add system prompt if present
        if system_prompt:
            payload["system"] = system_prompt

        response_data = await self.http_client.post_json(
            url=self.base_url,
            headers=self._build_headers(),
            json=payload,
            timeout=None,
        )

        return self._parse_response(response_data)

    def _separate_system_messages(
        self, messages: List[Message]
    ) -> Tuple[Optional[str], List[Message]]:
        """
        Extract system messages and return them separately.

        Anthropic expects system prompt as a separate field, not in messages array.

        Args:
            messages: All messages including potential system messages

        Returns:
            Tuple of (system_prompt, conversation_messages)
        """
        system_messages = []
        conversation_messages = []

        for msg in messages:
            if msg.role == "system":
                system_messages.append(msg.content)
            else:
                conversation_messages.append(msg)

        # Combine multiple system messages if present
        system_prompt = "\n\n".join(system_messages) if system_messages else None

        return system_prompt, conversation_messages

    def _to_anthropic_format(self, messages: List[Message]) -> List[dict[str, str]]:
        """
        Convert universal Message format to Anthropic API format.

        Args:
            messages: Messages in universal format

        Returns:
            Messages in Anthropic format
        """
        return [{"role": msg.role, "content": msg.content} for msg in messages]

    def _build_headers(self) -> dict[str, str]:
        """Build HTTP headers for Anthropic API request."""
        return {
            "x-api-key": self.api_key,
            "anthropic-version": self.ANTHROPIC_VERSION,
            "Content-Type": "application/json",
        }

    def _parse_response(self, response_data: dict[str, Any]) -> Message:
        """
        Parse Anthropic API response into universal Message format.

        Args:
            response_data: Raw API response

        Returns:
            Assistant message

        Raises:
            KeyError: If response format is unexpected
        """
        try:
            content = response_data["content"][0]["text"]
            return Message(role="assistant", content=content)
        except (KeyError, IndexError) as e:
            logger.error(f"Failed to parse Anthropic response: {response_data}")
            raise ValueError(f"Invalid Anthropic response format: {e}")
