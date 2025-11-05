"""
gRPC server implementation for the prompt-engineer portfolio.

This server implements the ModelService defined in the protos directory. It
provides two RPCs for running prompts: one that returns a simple
response and another that includes a mock trace of the processing steps.

The implementation uses the asyncio API of grpcio for demonstration
purposes. In production, you might use grpclib or another framework
depending on your requirements.
"""

import asyncio
from concurrent import futures
import grpc

from protos import model_service_pb2, model_service_pb2_grpc  # type: ignore


class ModelServiceServicer(model_service_pb2_grpc.ModelServiceServicer):
    async def RunPrompt(self, request, context):  # type: ignore
        # For demonstration, echo the prompt back prefixed with a message
        output = f"Model response: {request.prompt}"
        return model_service_pb2.PromptResponse(output=output)

    async def RunPromptWithTrace(self, request, context):  # type: ignore
        steps = [
            model_service_pb2.TraceStep(name="fill_template", detail=f"Prompt: {request.prompt}"),
            model_service_pb2.TraceStep(name="call_model", detail="Called mock model"),
            model_service_pb2.TraceStep(name="postprocess", detail="Returned response"),
        ]
        final_output = f"Model response: {request.prompt}"
        return model_service_pb2.TraceResponse(steps=steps, final_output=final_output)


async def serve() -> None:
    server = grpc.aio.server()
    model_service_pb2_grpc.add_ModelServiceServicer_to_server(ModelServiceServicer(), server)
    listen_addr = "0.0.0.0:50051"
    server.add_insecure_port(listen_addr)
    print(f"Starting gRPC server on {listen_addr}")
    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    asyncio.run(serve())