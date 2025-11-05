"""
Pydantic models used by the API.

This file defines data schemas shared across the REST API endpoints. Keeping
the schemas in a separate module encourages reuse and easier evolution
of the API contract.
"""

from pydantic import BaseModel
from typing import Any, Dict


class PromptRequest(BaseModel):
    prompt: str
    parameters: Dict[str, Any] | None = None


class PromptResponse(BaseModel):
    response: Dict[str, Any]


class TraceStep(BaseModel):
    step: str
    detail: str


class TraceResponse(PromptResponse):
    trace: list[TraceStep]