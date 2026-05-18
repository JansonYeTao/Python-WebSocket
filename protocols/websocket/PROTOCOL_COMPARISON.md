# WebSocket vs Other Protocols (HTTP, gRPC Streaming, WebRTC)

Date: 2026-05-15

This document compares WebSocket with common alternatives and gives concrete examples so you can choose the right protocol for each use case.

---

## 1) Quick comparison table

| Protocol | Direction | Typical transport | Best for | Main tradeoff |
|---|---|---|---|---|
| HTTP (request/response) | Client -> Server (per request) | HTTP/1.1 or HTTP/2 | CRUD APIs, low-frequency updates | Higher latency for realtime push patterns |
| HTTP polling | Simulated server push (client repeatedly asks) | HTTP | Simple near-realtime where scale is small | Wasted requests and overhead |
| WebSocket | Full-duplex (both directions anytime) | HTTP Upgrade -> WS frames over TCP | Chat, collaboration, event streams | More stateful operational complexity |
| gRPC streaming | Server/client/bidi streaming with typed RPC | HTTP/2 + Protobuf | Service-to-service streaming, strong contracts | Browser path usually needs grpc-web/proxy |
| WebRTC DataChannel | Peer-to-peer bidirectional data | SCTP/DTLS/UDP (via ICE/STUN/TURN) | P2P realtime data/media-adjacent use | NAT traversal/signaling complexity |

---

## 2) WebSocket vs HTTP (request/response & polling)

### Mental model
- HTTP: each interaction is a separate request/response lifecycle.
- WebSocket: one long-lived connection where both sides can send at any time.

### Example

#### HTTP polling
Client asks every 2 seconds:

```http
GET /poll?payload=hello
```

Server replies:

```json
{"reversed_data":"olleh","status":"ok"}
```

#### WebSocket
Client connects once to `/ws`, then sends many messages over same connection:

```json
"hello"
```

Server responds:

```json
{"reversed_data":"olleh","status":"ok"}
```

In this repo, both endpoints exist with matching semantics for comparison:
- `GET /poll`
- `WS /ws`

See: `protocols/websocket/server/listen.py`.

### When HTTP is better
- Infrequent updates
- Simpler infra and observability needs
- Existing REST-heavy architecture

### When WebSocket is better
- Bidirectional realtime interaction
- High message frequency
- Low-latency UX targets

---

## 3) WebSocket vs gRPC Streaming

### Mental model
- WebSocket: transport channel; app message schema is your responsibility.
- gRPC streaming: typed RPC method with schema-first contract via `.proto`.

### Example

#### WebSocket message envelope (app-defined)

```json
{
  "type": "chat.message",
  "room_id": "r1",
  "user_id": "u1",
  "text": "hi"
}
```

#### gRPC `.proto` definition (schema-first)

```proto
syntax = "proto3";

service ChatService {
  rpc ChatStream (stream ChatMessage) returns (stream ChatMessage);
}

message ChatMessage {
  string room_id = 1;
  string user_id = 2;
  string text = 3;
  int64 ts = 4;
}
```

### When gRPC streaming is better
- Service-to-service communication
- Strong typed contracts and codegen desired
- Multi-language backend ecosystems

### When WebSocket is better
- Browser-native realtime without grpc-web proxy stack
- Flexible event schemas that evolve quickly

---

## 4) WebSocket vs WebRTC

### Mental model
- WebSocket: client-server realtime pipe.
- WebRTC: peer-to-peer realtime media/data (after signaling).

### Example
- Multiplayer game state via central authoritative server -> WebSocket often simpler.
- Direct peer data exchange (or audio/video) -> WebRTC is typically more appropriate.

### When WebRTC is better
- P2P media/data with low-latency direct paths
- Use cases already requiring ICE/STUN/TURN stack

### When WebSocket is better
- Centralized control plane
- Easier server-side enforcement, logging, moderation, auditing

---

## 5) Decision cheat-sheet

Choose **HTTP/REST** when:
- request/response fits naturally
- update frequency is low

Choose **WebSocket** when:
- client and server both need to push events
- realtime UX is core

Choose **gRPC streaming** when:
- backend services need efficient, typed streaming RPC

Choose **WebRTC** when:
- peer-to-peer data/media path is the product requirement

---

## 6) Related docs in this repo

- WebSocket benchmark plan: `protocols/websocket/benchmarks/PLAN.md`
- Benchmark results summary: `protocols/websocket/benchmarks/REPORT.md`
- WebSocket tradeoff costs: `protocols/websocket/benchmarks/TRADEOFFS.md`
- From-scratch WebSocket internals: `protocols/websocket/scratch_ws/README.md`
