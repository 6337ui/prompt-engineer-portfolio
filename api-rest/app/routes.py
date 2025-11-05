"""
Route definitions for the REST API.

These routes expose endpoints for running prompts against a cloud
language model and returning either the raw response or a detailed
trace of the interaction. The underlying model calls are handled
through the httpx-client defined in the httpx-client package.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Any, Dict
import asyncio

from httpx_client.model_client import call_model  # type: ignore


router = APIRouter()


class PromptRequest(BaseModel):
    prompt: str
    parameters: Dict[str, Any] | None = None


@router.post("/prompt/run")
async def run_prompt(req: PromptRequest) -> Dict[str, Any]:
    """Run a prompt through the cloud model and return the raw response."""
    try:
        result = await call_model(req.prompt, req.parameters)
        return {"response": result}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/prompt/trace")
async def run_prompt_with_trace(req: PromptRequest) -> Dict[str, Any]:
    """Run a prompt and return a mock trace for demonstration purposes."""
    # In a real implementation, this would capture detailed steps.
    result = await run_prompt(req)
    trace = [
        {"step": "fill_template", "detail": f"Filled template with prompt: {req.prompt}"},
        {"step": "http_request", "detail": "Called cloud model"},
        {"step": "postprocess", "detail": "Returned response unchanged"},
    ]
    return {"response": result["response"], "trace": trace}


@router.get("/examples")
async def get_examples() -> Dict[str, Any]:
    """Return a small set of example prompts for demonstration."""
    return {
        "examples": [
            {"id": "ex1", "prompt": "Translate to French: Hello, world"},
            {"id": "ex2", "prompt": "Summarise the following text..."},
        ]
    }