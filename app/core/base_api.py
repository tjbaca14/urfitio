import logging
from abc import ABC, abstractmethod

import httpx
from fastapi import HTTPException

class BaseApi(ABC):

    def __init__(self, http_client: httpx.AsyncClient) -> None:
        self._http_client = http_client

    @abstractmethod
    async def generate(self):
        pass

    async def _post(
        self, url: str, headers: dict, data: dict, logger: logging.Logger
    ) -> dict:
        try:
            response = await self._http_client.post(
                url=url, headers=headers, json=data, timeout=None
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.exception(f"Unable to complete request: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
