import logging
from typing import Any

import httpx
from fastapi import HTTPException


class HTTPClient:
    """
    Generic HTTP client with error handling and logging.

    Wraps httpx.AsyncClient to provide consistent error handling,
    logging, and exception translation across all HTTP integrations.
    """

    def __init__(self, client: httpx.AsyncClient, logger: logging.Logger):
        """
        Initialize HTTP client.

        Args:
            client: Shared httpx.AsyncClient instance
            logger: Logger for this client
        """
        self._client = client
        self._logger = logger

    async def post(
        self,
        url: str,
        headers: dict[str, str],
        json: dict[str, Any],
        timeout: float | None = None,
    ) -> dict:
        """
        Make POST request with comprehensive error handling.

        Args:
            url: Target URL
            headers: HTTP headers
            json: JSON payload
            timeout: Optional request timeout in seconds

        Returns:
            Response JSON as dictionary

        Raises:
            HTTPException: On any HTTP, network, or unexpected error
        """
        try:
            response = await self._client.post(
                url=url, headers=headers, json=json, timeout=timeout
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            self._logger.error(
                f"HTTP {e.response.status_code} error: {e.response.text}"
            )
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"API error: {e.response.text}",
            )
        except httpx.RequestError as e:
            self._logger.error(f"Network error: {str(e)}")
            raise HTTPException(
                status_code=503, detail=f"Service unavailable: {str(e)}"
            )
        except Exception as e:
            self._logger.exception(f"Unexpected error: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

    async def get(
        self,
        url: str,
        headers: dict[str, str] | None = None,
        params: dict[str, Any] | None = None,
        timeout: float | None = None,
    ) -> dict:
        """
        Make GET request with comprehensive error handling.

        Args:
            url: Target URL
            headers: Optional HTTP headers
            params: Optional query parameters
            timeout: Optional request timeout in seconds

        Returns:
            Response JSON as dictionary

        Raises:
            HTTPException: On any HTTP, network, or unexpected error
        """
        try:
            response = await self._client.get(
                url=url, headers=headers or {}, params=params, timeout=timeout
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            self._logger.error(
                f"HTTP {e.response.status_code} error: {e.response.text}"
            )
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"API error: {e.response.text}",
            )
        except httpx.RequestError as e:
            self._logger.error(f"Network error: {str(e)}")
            raise HTTPException(
                status_code=503, detail=f"Service unavailable: {str(e)}"
            )
        except Exception as e:
            self._logger.exception(f"Unexpected error: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
