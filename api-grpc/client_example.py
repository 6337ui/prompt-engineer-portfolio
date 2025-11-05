"""
Example gRPC client for the prompt-engineer portfolio.

This script demonstrates how to call the ModelService exposed by the
gRPC server. It connects to the server, sends a prompt, and prints
the response. The example uses the asyncio API of grpcio.
"""

import asyncio
import grpc

from protos import model_service_pb2, model_service_pb2_grpc  # type: ignore


async def run_client() -> None:
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = model_service_pb2_grpc.ModelServiceStub(channel)
        request = model_service_pb2.PromptRequest(prompt="Hello")
        response = await stub.RunPrompt(request)
        print("Received:", response.output)


if __name__ == "__main__":
    asyncio.run(run_client())