# TODO

This file lists potential improvements and next steps for the prompt
engineer portfolio.  It serves as a lightweight backlog to guide
future development and to demonstrate awareness of further work that
could be done beyond the core skeleton.

- [ ] **Generate gRPC stubs**: Use `grpcio-tools` or `protoc` to
  generate the Python stubs from `api-grpc/protos/model_service.proto`.
  These generated files (`model_service_pb2.py` and
  `model_service_pb2_grpc.py`) should be committed so the gRPC
  server can run without requiring code generation at runtime.
- [ ] **Expand metric suite**: Add additional metrics to
  `trace-eval/metrics.py`, such as semantic similarity (using
  sentence embeddings) and simple safety checks.
- [ ] **Web UI**: Build a minimal web interface to test prompt
  templates and display traces.  This could live in a new
  `playground` directory and leverage the existing REST API.
- [ ] **Deployment documentation**: Extend the documentation to
  describe how to deploy the services to a cloud provider (e.g.,
  Docker Hub + Kubernetes or serverless options).