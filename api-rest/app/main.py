"""
FastAPI application for the prompt-engineer portfolio.

This module creates a minimal FastAPI app and includes routes defined
in the routes module. It serves as an entry point for the REST API
service, which wraps calls to a cloud language model via httpx.

The app is kept deliberately simple to focus on illustrating
architectural patterns rather than providing a production-ready API.
"""

from fastapi import FastAPI
from .routes import router


def create_app() -> FastAPI:
    """Create and configure the FastAPI app."""
    app = FastAPI(title="Prompt Engineer Portfolio - REST API")
    app.include_router(router, prefix="/v1")
    return app


app = create_app()