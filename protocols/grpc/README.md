# gRPC Protocol Track

This track introduces gRPC and gRPC streaming (unary, server streaming, bidi streaming).

## What you'll learn

- Schema-first API design with `.proto`
- Unary RPC vs streaming RPC mental model
- Service-to-service typed contracts
- How gRPC streaming compares to WebSocket transport messaging

## Structure

```text
protocols/grpc/
├── protos/
│   └── chat.proto
├── server/
│   └── service.py
└── clients/
    └── client.py
```

## Install additional dependencies

```bash
pip install grpcio grpcio-tools
```

## Generate Python code from proto

Run from repo root:

```bash
python -m grpc_tools.protoc \
  -I . \
  --python_out=. \
  --grpc_python_out=. \
  protocols/grpc/protos/chat.proto
```

This generates:
- `protocols/grpc/protos/chat_pb2.py`
- `protocols/grpc/protos/chat_pb2_grpc.py`

## Run server

```bash
python protocols/grpc/server/service.py
```

## Run client examples

```bash
python protocols/grpc/clients/client.py
```

## Notes

- gRPC streaming is excellent for backend service-to-service typed streams.
- Browser direct support is usually done through grpc-web + proxy.
- For browser-native bidirectional realtime, see `protocols/websocket/`.
