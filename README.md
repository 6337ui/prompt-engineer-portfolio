# Prompt Engineer Portfolio

This repository collects a set of components that demonstrate skills
related to prompt engineering, model integration and evaluation. It is
intended as a portfolio to showcase how one might structure projects
around interacting with large language models using REST and gRPC
APIs, build chains with LangChain, and evaluate prompts systematically.

## Contents

* **api-rest** – FastAPI service that wraps a cloud language model. It
  provides endpoints to run prompts and retrieve traces.
* **api-grpc** – gRPC service using Protocol Buffers to define an
  interface for running prompts.
* **httpx-client** – Async client module for calling the cloud model
  via `httpx`.
* **langchain-examples** – Example LangChain chains and prompt
  templates.
* **trace-eval** – Harness to run evaluation cases, collect traces
  and compute simple metrics.
* **docs** – Architecture overview and other documentation.
* **docker-compose.yml** – Compose file to spin up the services and a
  mock model for local testing.

## Getting Started

```bash
# Install dependencies for the REST API
cd api-rest
pip install -r requirements.txt

# Run the REST API
uvicorn app.main:app --reload

# Run the gRPC server
cd ../api-grpc
python server.py

# Run the trace evaluation harness
cd ../trace-eval
python harness.py
```

Alternatively, use Docker Compose to build and run all services:

```bash
make up
```

This will start the REST API on port 8000, the gRPC server on port
50051 and a simple mock model on port 8080.

## License

This project is licensed under the MIT License. See the `LICENSE` file
for details.