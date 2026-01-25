from typing import List

from app.common.models import Message
from app.integrations.llm.base import LLMProvider


class SimpleGenerator:

    def __init__(self, llm_provider: LLMProvider) -> None:
        self.llm_provider = llm_provider

    async def generate(
        self,
        messages: List[Message],
        temperature: float = 0.7,
        max_tokens: int = 1024,
    ) -> Message:
        return await self.llm_provider.invoke(
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
