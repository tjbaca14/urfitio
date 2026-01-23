from __future__ import annotations

import json as jsonlib
import logging
from typing import Any, Mapping

import httpx
from app.common.clients.errors import (NetworkError, ResponseParseError,
                                       UnexpectedClientError,
                                       UpstreamHTTPError)


class HTTPClient:
    """
    Generic HTTP client with error handling and logging.

    Wraps httpx.AsyncClient to provide consistent error handling, logging,
    and exception translation across all HTTP integrations.

    Important: This client must not raise FastAPI exceptions. Translate at the API boundary.
    """

    def __init__(self, client: httpx.AsyncClient, logger: logging.Logger):
        self._client = client
        self._logger = logger

    async def post_json(
        self,
        url: str,
        headers: Mapping[str, str],
        json: Mapping[str, Any],
        timeout: float | None = None,
    ) -> dict[str, Any]:
        return await self._request_json(
            method="POST",
            url=url,
            headers=headers,
            json=json,
            params=None,
            timeout=timeout,
        )

    async def get_json(
        self,
        url: str,
        headers: Mapping[str, str] | None = None,
        params: Mapping[str, Any] | None = None,
        timeout: float | None = None,
    ) -> dict[str, Any]:
        return await self._request_json(
            method="GET",
            url=url,
            headers=headers or {},
            json=None,
            params=params,
            timeout=timeout,
        )

    async def _request_json(
        self,
        method: str,
        url: str,
        headers: Mapping[str, str],
        json: Mapping[str, Any] | None,
        params: Mapping[str, Any] | None,
        timeout: float | None,
    ) -> dict[str, Any]:
        try:
            response = await self._client.request(
                method=method,
                url=url,
                headers=dict(headers),
                json=dict(json) if json is not None else None,
                params=dict(params) if params is not None else None,
                timeout=timeout,
            )

            # Raise for non-2xx
            response.raise_for_status()

            # Parse JSON
            try:
                data = response.json()
            except (ValueError, jsonlib.JSONDecodeError) as e:
                text = response.text
                self._logger.error(f"Failed to parse JSON from {method} {url}: {text}")
                raise ResponseParseError(
                    message="Invalid JSON response from upstream",
                    response_text=text,
                ) from e

            # Ensure dict for downstream expectations
            if not isinstance(data, dict):
                self._logger.error(
                    f"Expected JSON object (dict) from {method} {url}, got {type(data)}"
                )
                raise ResponseParseError(
                    message="Unexpected JSON shape from upstream (expected object)",
                    response_text=response.text,
                )

            return data

        except httpx.HTTPStatusError as e:
            code = e.response.status_code
            text = e.response.text
            self._logger.error(f"Upstream HTTP error {code} for {method} {url}: {text}")

            # Basic retryability heuristic
            retryable = code in {408, 429, 500, 502, 503, 504}

            raise UpstreamHTTPError(
                message="Upstream API returned an error response",
                status_code=code,
                response_text=text,
                is_retryable=retryable,
            ) from e

        except httpx.RequestError as e:
            # DNS, connect, timeout, etc.
            self._logger.error(f"Network error for {method} {url}: {str(e)}")
            raise NetworkError(
                message=f"Network error contacting upstream: {str(e)}"
            ) from e

        except (UpstreamHTTPError, NetworkError, ResponseParseError):
            # Already normalized
            raise

        except Exception as e:
            self._logger.exception(
                f"Unexpected HTTP client error for {method} {url}: {str(e)}"
            )
            raise UnexpectedClientError(
                message="Unexpected client error", original=e
            ) from e
