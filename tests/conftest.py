"""Pytest configuration file for fixtures."""

import json
import pytest
from pathlib import Path


@pytest.fixture(scope="session")
def mock_model_response(tmp_path_factory):
    """Return a path to a mock model response JSON file."""
    data = {"output": "Mock response"}
    path = tmp_path_factory.mktemp("data") / "response.json"
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh)
    return path