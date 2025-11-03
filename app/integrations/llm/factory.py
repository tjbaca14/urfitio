from app.common.clients.http_client import HTTPClient
from app.settings import LLMConfig
from app.integrations.llm.anthropic import AnthropicProvider
from app.integrations.llm.base import BaseLLMProvider


class LLMProviderFactory:
    """
    Factory for creating LLM provider instances.

    Centralizes provider instantiation and configuration.
    """

    provider_map = {
        "anthropic": AnthropicProvider,
    }

    @staticmethod
    def create(config: LLMConfig, http_client: HTTPClient) -> BaseLLMProvider:
        """
        Create LLM provider based on provider name.

        Args:
            provider_name: Provider identifier ("anthropic", "openai", etc.)
            config: LLM configuration
            http_client: HTTP client for making requests

        Returns:
            Configured LLM provider instance

        Raises:
            ValueError: If provider_name is not recognized
        """
        provider_name = config.PROVIDER.lower()

        provider_class = LLMProviderFactory.provider_map.get(provider_name)

        if not provider_class:
            supported = ", ".join(LLMProviderFactory.provider_map.keys())
            raise ValueError(
                f"Unknown LLM provider: {provider_name}. "
                f"Supported providers: {supported}"
            )

        return provider_class(
            api_key=config.API_KEY,
            model=config.MODEL,
            base_url=config.URL,
            http_client=http_client,
        )
