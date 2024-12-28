from typing import List

import httpx
from fastapi import HTTPException

from app.config import ClaudeConfig
from app.models.chat import Message
from app.models.claude_request import ClaudeRequest
from app.util import get_logger

logger = get_logger(__name__)


class ClaudeAPI:

    def __init__(self, config: ClaudeConfig, http_client: httpx.AsyncClient) -> None:
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

        claude_request = ClaudeRequest(
            model=self._config.MODEL,
            max_tokens=self._config.MAX_TOKENS,
            system=system,
            temperature=self._config.TEMPERATURE,
            messages=messages,
        )
        response = await self._post(headers=headers, data=claude_request.model_dump())
        return Message(role="assistant", content=response["content"][0]["text"])

    async def _post(self, headers: dict, data: dict) -> dict:

        try:
            response = await self._http_client.post(
                url=self._config.URL, headers=headers, json=data, timeout=None
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.exception(f"Unable to complete request: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
