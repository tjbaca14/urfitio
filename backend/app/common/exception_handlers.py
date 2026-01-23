from __future__ import annotations

from app.common.clients.errors import (NetworkError, ResponseParseError,
                                       UnexpectedClientError,
                                       UpstreamHTTPError)
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(UpstreamHTTPError)
    async def handle_upstream_http_error(_: Request, exc: UpstreamHTTPError):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.response_text},
        )

    @app.exception_handler(NetworkError)
    async def handle_network_error(_: Request, exc: NetworkError):
        return JSONResponse(
            status_code=503,
            content={"detail": "Upstream service unavailable"},
        )

    @app.exception_handler(ResponseParseError)
    async def handle_parse_error(_: Request, exc: ResponseParseError):
        return JSONResponse(
            status_code=502,
            content={"detail": "Invalid response from upstream service"},
        )

    @app.exception_handler(UnexpectedClientError)
    async def handle_unexpected_client_error(_: Request, exc: UnexpectedClientError):
        return JSONResponse(
            status_code=500,
            content={"detail": "Unexpected internal error"},
        )
