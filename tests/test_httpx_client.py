"""Tests for the httpx-based model client."""

import asyncio
import httpx
import pytest
from httpx_client.model_client import call_model


class MockTransport(httpx.AsyncBaseTransport):
    async def handle_async_request(self, request: httpx.Request) -> httpx.Response:
        assert request.method == "POST"
        return httpx.Response(200, json={"output": "OK"})


@pytest.mark.asyncio
async def test_call_model(monkeypatch):
    transport = MockTransport()
    async with httpx.AsyncClient(transport=transport) as client:
        monkeypatch.setattr(httpx, "AsyncClient", lambda *a, **k: client)
        result = await call_model("Hello")
    assert result["output"] == "OK"