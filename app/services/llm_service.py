from typing import List

import httpx

from app.core.base_api import BaseApi
from app.core.config import LLMConfig
from app.models.chat import Message
from app.models.llm_request import LLMRequest
from app.util import get_logger

logger = get_logger(__name__)


class LLMApi(BaseApi):

    def __init__(self, config: LLMConfig, http_client: httpx.AsyncClient) -> None:
        self._config = config
        self._http_client = http_client

    async def generate(
        self, messages: List[Message], system: str | None = None
    ) -> Message:
        headers = {
            "x-api-key": self._config.API_KEY,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json",
        }
        system = """Use the provided context to answer the usery query.
                    If the question cannot be answered from the provided context do not answer, inform the user as such and prompt a new question.
                    If a user asks a question pertaining for themselves ask for more data to answer the questino to the best of your ability.
                    """  # TODO: fix system prompt

        llm_request = LLMRequest(
            model=self._config.MODEL,
            max_tokens=self._config.MAX_TOKENS,
            system=system,
            temperature=self._config.TEMPERATURE,
            messages=messages,
        )
        response = await self._post(
            url=self._config.URL,
            headers=headers,
            data=llm_request.model_dump(),
            logger=logger,
        )
        return Message(role="assistant", content=response["content"][0]["text"])
