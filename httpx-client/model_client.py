"""
Async client for calling a cloud-based language model via HTTP.

This module wraps httpx to provide a simple interface for sending
prompts to a remote language model endpoint. The URL and API key are
supplied via environment variables to keep sensitive details out of
source control. In a real project, you might want to handle retries,
backoff and error logging more comprehensively.
"""

import os
from typing import Any, Dict
import httpx

API_URL = os.getenv("LLM_API_URL", "https://example.com/v1/generate")
API_KEY = os.getenv("LLM_API_KEY", "test-key")


async def call_model(prompt: str, params: Dict[str, Any] | None = None) -> Dict[str, Any]:
    """Send a prompt to the language model and return the JSON response."""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    payload: Dict[str, Any] = {"prompt": prompt}
    if params:
        payload.update(params)
    async with httpx.AsyncClient() as client:
        response = await client.post(API_URL, json=payload, headers=headers, timeout=30.0)
        response.raise_for_status()
        return response.json()