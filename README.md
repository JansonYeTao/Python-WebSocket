# Network Protocol Tutorial Repo

A beginner-friendly, practical network protocol tutorial in Python with:

- a **FastAPI WebSocket server**
- a **browser chat page**
- a **Python CLI client**
- clear notes on **how WebSocket works** and **when to use it**

If you want a cool repo to link on your personal blog, this project is built to be easy to clone, run, and explain.

---

## 0) Why this repo name

This repository now frames WebSocket as part of a broader **network protocol learning track**:

- HTTP request/response baseline
- HTTP Upgrade to WebSocket
- WebSocket frame parsing (from scratch)
- transport tradeoffs (WebSocket vs HTTP polling)

So the focus is not only application code, but protocol-level thinking.


## 1) What you’ll learn

By the end, you’ll understand:

1. How WebSocket differs from HTTP polling and REST.
2. The handshake idea (`Upgrade` → `101 Switching Protocols`).
3. Message flow in a persistent bidirectional connection.
4. Tradeoffs for common real-world use cases.

---

## 2) Quick start

### Prerequisites

- Python 3.10+

### Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Run the server

```bash
uvicorn protocols.websocket.server.listen:app --host 0.0.0.0 --port 8000 --reload
```

### Try it in browser

Open:

- `http://localhost:8000/`

Type a message and press **Send**. The server returns a JSON response with the reversed text.

### Try it in Python (CLI client)

In another terminal (with venv activated):

```bash
python protocols/websocket/clients/myclient.py
```

Type messages in the terminal. The client will send JSON over WebSocket and print server replies.

---

## 3) Repo structure

```text
.
├── protocols/
│   └── websocket/
│       ├── server/
│       │   └── listen.py      # FastAPI app + WebSocket endpoint
│       ├── clients/
│       │   └── myclient.py    # Async Python CLI WebSocket client
│       ├── benchmarks/
│       └── scratch_ws/
├── requirements.txt
└── README.md
```

---

## 4) How this demo works

### Server side (`/ws`)

- Accepts a WebSocket connection.
- Sends an initial JSON status.
- Loops forever receiving JSON messages.
- Returns:
  - `reversed_data`: reverse of input
  - `status`: simple success marker

This keeps the tutorial focused on connection lifecycle and message exchange.

### Browser page (`/`)

- Opens WebSocket to `ws://localhost:8000/ws`
- Sends typed messages
- Appends each server response to a list

### Python CLI client

- Connects to the same endpoint
- Runs a send + receive loop in terminal
- Good for understanding behavior without a browser

---

## 5) WebSocket tradeoffs (use-case chooser)

### Use WebSocket when

- You need **real-time** updates.
- You need **bidirectional** communication.
- You exchange frequent small messages (chat, collaboration, game events).

### Prefer SSE when

- You mostly need **server → client** streaming only (notifications, feeds).

### Prefer REST/polling when

- Updates are infrequent.
- Simplicity and standard HTTP tooling matter more than low latency.

### Key operational tradeoffs with WebSocket

- More complex scaling (many long-lived connections).
- Need heartbeat/reconnect logic.
- Need backpressure strategy for slow clients.

---

## 6) Blog-friendly tutorial flow

If you’re writing a personal blog post, a strong structure is:

1. Introduce the problem (why HTTP polling feels limited).
2. Explain WebSocket mental model (persistent “phone call”).
3. Run this repo in 3 steps.
4. Show one request/response example in browser + CLI.
5. Discuss tradeoffs (WebSocket vs SSE vs REST).
6. End with next steps (auth, rooms, Redis pub/sub, deployment).

---

## 7) Next improvements you can add

- Message envelope schema: `{type, id, ts, payload}`
- Room support (multi-user chat)
- Token-based auth
- Ping/pong heartbeat
- Reconnect logic in browser client
- Redis pub/sub for multi-instance scale

---

## License

Use freely for learning and blog/tutorial content.


---

## Benchmark-first track (WebSocket vs HTTP)

Before implementing a full from-scratch tutorial, use the benchmark plan in `protocols/websocket/benchmarks/PLAN.md` to measure when WebSocket is beneficial versus overkill.

- Plan file: `protocols/websocket/benchmarks/PLAN.md`
- Includes scenarios, metrics, methodology, and chart outputs for blog-ready visualization.

This keeps architectural decisions evidence-based and makes your tutorial stronger with real data.


## 8) Run actual benchmark now

Start the server:

```bash
uvicorn protocols.websocket.server.listen:app --host 0.0.0.0 --port 8000
```

In a second terminal, run the benchmark script:

```bash
python protocols/websocket/benchmarks/run_benchmark.py --base-url http://127.0.0.1:8000 --clients 20 --messages 20 --payload-size 128 --transport both
```

This produces JSON results at `protocols/websocket/benchmarks/results/latest.json` with:
- throughput (messages/sec)
- latency p50/p95/p99 and mean
- success counts and duration

Tip: run multiple passes for your blog:

```bash
python protocols/websocket/benchmarks/run_benchmark.py --clients 10 --messages 50 --payload-size 64 --transport both --output protocols/websocket/benchmarks/results/c10_p64.json
python protocols/websocket/benchmarks/run_benchmark.py --clients 100 --messages 50 --payload-size 1024 --transport both --output protocols/websocket/benchmarks/results/c100_p1024.json
```


## 9) Detailed tradeoff costs

For a focused breakdown of what you *pay* when choosing WebSocket (operational, scaling, backpressure, auth, observability), see:

- `protocols/websocket/benchmarks/TRADEOFFS.md`


## 10) From-scratch WebSocket track (mental model)

For deeper understanding, start with the educational raw-socket implementation:

- `protocols/websocket/scratch_ws/README.md`
- `protocols/websocket/scratch_ws/handshake_server.py`
- `protocols/websocket/scratch_ws/frame_echo_server.py`
- `protocols/websocket/scratch_ws/helpers.py`

This track helps you learn:
1. TCP socket acceptance
2. HTTP upgrade handshake (`101`)
3. Frame parsing/unmasking
4. Server text frame encoding

Then compare with `protocols/websocket/server/listen.py` to see what frameworks abstract away.


## 11) Protocol comparison guide

For side-by-side comparison with examples (WebSocket vs HTTP, gRPC streaming, WebRTC), see:

- `protocols/websocket/PROTOCOL_COMPARISON.md`
