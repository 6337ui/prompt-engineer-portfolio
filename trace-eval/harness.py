"""
Trace evaluation harness for the prompt-engineer portfolio.

This script provides a minimal framework for running a set of prompts
through the system and collecting structured traces and metrics. It
loads test cases from a JSON file, runs each prompt using the
httpx-client, records timing information and outputs per-run JSON
objects into the `traces` directory.
"""

import json
import os
import time
from pathlib import Path
from typing import Dict, Any

import asyncio

from httpx_client.model_client import call_model  # type: ignore
from .metrics import compute_metrics


def load_examples(path: str) -> list[Dict[str, Any]]:
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


async def run_case(case: Dict[str, Any]) -> Dict[str, Any]:
    start = time.perf_counter()
    response = await call_model(case["prompt"])
    latency = (time.perf_counter() - start) * 1000
    trace = [
        {"step": "http_request", "detail": "Called cloud model"},
    ]
    metrics = compute_metrics(case.get("expected", ""), response.get("output", ""))
    return {
        "id": case["id"],
        "prompt": case["prompt"],
        "response": response,
        "latency_ms": latency,
        "trace": trace,
        "metrics": metrics,
    }


async def main() -> None:
    examples = load_examples(os.path.join(Path(__file__).parent, "examples.json"))
    traces_dir = Path(__file__).parent / "traces"
    traces_dir.mkdir(exist_ok=True)
    results = []
    for case in examples:
        result = await run_case(case)
        results.append(result)
        out_path = traces_dir / f"{case['id']}.json"
        with open(out_path, "w", encoding="utf-8") as fh:
            json.dump(result, fh, indent=2)
    print(f"Processed {len(results)} cases and wrote trace files to {traces_dir}")


if __name__ == "__main__":
    asyncio.run(main())