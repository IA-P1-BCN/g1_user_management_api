"""JSON logging and per-request log metadata."""

import json
import logging

import httpx
from fastapi import FastAPI
from httpx import ASGITransport

from src.logging_config import JSONFormatter, RequestLoggingMiddleware


def test_log_record_formats_as_parseable_json_with_level_message_timestamp() -> None:
    formatter = JSONFormatter()
    record = logging.makeLogRecord(
        {"levelno": logging.INFO, "levelname": "INFO", "msg": "hello %s", "args": ("world",)}
    )

    payload = json.loads(formatter.format(record))

    assert payload["level"] == "INFO"
    assert payload["message"] == "hello world"
    assert payload["timestamp"]


async def test_http_request_is_logged_with_id_route_status_duration(caplog) -> None:
    app = FastAPI()
    app.add_middleware(RequestLoggingMiddleware)

    @app.get("/ping")
    async def ping() -> dict[str, str]:
        return {"pong": "yes"}

    with caplog.at_level(logging.INFO):
        transport = ASGITransport(app=app)
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.get("/ping")

    assert response.status_code == 200
    assert response.headers["x-request-id"]

    record = next(r for r in caplog.records if r.name == "request")
    assert record.route == "/ping"
    assert record.status == 200
    assert isinstance(record.duration_ms, float)
    assert record.request_id == response.headers["x-request-id"]
