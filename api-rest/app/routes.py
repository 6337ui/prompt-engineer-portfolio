"""
Route definitions for the REST API.

These routes expose endpoints for running prompts against a cloud
language model and returning either the raw response or a detailed
trace of the interaction. The underlying model calls are handled
through the httpx-client defined in the httpx-client package.
"""

"""
Route definitions for the REST API.

These routes expose endpoints for running prompts against a cloud
language model and returning either the raw response or a detailed
trace of the interaction.  Schemas are imported from the local
``schemas`` module to keep the API contract in one place.
"""

from fastapi import APIRouter, HTTPException
from typing import Any, Dict

from .schemas import (
    PromptRequest,
    PromptResponse,
    TraceResponse,
    TraceStep,
)

from httpx_client.model_client import call_model  # type: ignore


router = APIRouter()


@router.post("/prompt/run", response_model=PromptResponse)
async def run_prompt(req: PromptRequest) -> PromptResponse:
    """
    Run a prompt through the cloud model and return the raw response.

    The underlying HTTP call is delegated to ``call_model``.  Any exceptions
    raised by the client are converted into 500 responses.
    """
    try:
        result = await call_model(req.prompt, req.parameters)
        return PromptResponse(response=result)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/prompt/trace", response_model=TraceResponse)
async def run_prompt_with_trace(req: PromptRequest) -> TraceResponse:
    """
    Run a prompt and return a synthetic trace for demonstration purposes.

    A real implementation would capture intermediate steps such as template filling,
    network calls and post‐processing.  Here we construct a simple list of
    ``TraceStep`` instances to illustrate the shape of the response.
    """
    # Call the model via the existing run_prompt endpoint to reuse error handling.
    result = await run_prompt(req)
    trace = [
        TraceStep(step="fill_template", detail=f"Filled template with prompt: {req.prompt}"),
        TraceStep(step="http_request", detail="Called cloud model"),
        TraceStep(step="postprocess", detail="Returned response unchanged"),
    ]
    return TraceResponse(response=result.response, trace=trace)


@router.get("/examples")
async def get_examples() -> Dict[str, Any]:
    """Return a small set of example prompts for demonstration."""
    return {
        "examples": [
            {"id": "ex1", "prompt": "Translate to French: Hello, world"},
            {"id": "ex2", "prompt": "Summarise the following text..."},
        ]
    }