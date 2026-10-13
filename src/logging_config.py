"""Structured JSON logging and per-request log metadata."""

import json
import logging
import time
import uuid
from collections.abc import Awaitable, Callable
from typing import Any

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

_RESERVED_KEYS = set(logging.makeLogRecord({}).__dict__) | {"message", "asctime", "taskName"}


class JSONFormatter(logging.Formatter):
    """Format a log record as one parseable JSON line with level, message and timestamp."""

    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "timestamp": self.formatTime(record, "%Y-%m-%dT%H:%M:%S%z"),
            "level": record.levelname,
            "message": record.getMessage(),
        }
        for key, value in record.__dict__.items():
            if key not in _RESERVED_KEYS and not key.startswith("_"):
                payload[key] = value
        if record.exc_info:
            payload["exc_info"] = self.formatException(record.exc_info)
        return json.dumps(payload, default=str)


def configure_logging() -> None:
    """Route root logging through the JSON formatter."""
    handler = logging.StreamHandler()
    handler.setFormatter(JSONFormatter())
    root = logging.getLogger()
    root.handlers = [handler]
    root.setLevel(logging.INFO)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Log every HTTP request with a request id, route, status code and duration."""

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        request_id = uuid.uuid4().hex
        start = time.perf_counter()
        try:
            response = await call_next(request)
        except Exception:
            logging.getLogger("request").exception(
                "request failed",
                extra={
                    "request_id": request_id,
                    "route": request.url.path,
                    "status": 500,
                    "duration_ms": round((time.perf_counter() - start) * 1000, 2),
                },
            )
            raise
        duration_ms = round((time.perf_counter() - start) * 1000, 2)
        logging.getLogger("request").info(
            "request completed",
            extra={
                "request_id": request_id,
                "route": request.url.path,
                "status": response.status_code,
                "duration_ms": duration_ms,
            },
        )
        response.headers["X-Request-ID"] = request_id
        return response
