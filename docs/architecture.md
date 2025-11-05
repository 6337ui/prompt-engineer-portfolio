# Architecture Overview

This document outlines the high-level architecture of the prompt
engineer portfolio. The repository is organised into modular
components, each showcasing different aspects of prompt engineering
and language model integration:

* **api-rest**: A FastAPI-based REST service that wraps the cloud
  language model. This service exposes endpoints for running prompts
  and retrieving traces.
* **api-grpc**: A gRPC service exposing similar functionality via
  Protocol Buffers. It illustrates how to define services and
  messages using `proto3` and implement asynchronous servers in
  Python.
* **httpx-client**: A thin asynchronous client around `httpx` for
  making calls to an external language model API. It centralises
  configuration and error handling.
* **langchain-examples**: Demonstrates how to use LangChain to build
  chains and integrate a custom LLM wrapper.
* **trace-eval**: Provides a harness for running evaluation cases and
  collecting structured traces. It includes basic metrics to compare
  outputs.

Each component is containerised with Docker and orchestrated via
`docker-compose`. The repository includes a GitHub Actions workflow
for continuous integration.