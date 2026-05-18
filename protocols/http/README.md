# HTTP Protocol Track

This track introduces HTTP fundamentals with runnable examples.

## What you'll learn

- Request/response mental model
- Stateless interaction patterns
- Polling basics and tradeoffs
- How HTTP compares to WebSocket for realtime use cases

## Structure

```text
protocols/http/
├── server/
│   └── app.py
└── clients/
    └── poll_client.py
```

## Run server

```bash
uvicorn protocols.http.server.app:app --host 0.0.0.0 --port 8080 --reload
```

## Try endpoints

```bash
curl http://127.0.0.1:8080/health
curl http://127.0.0.1:8080/items/1
curl 'http://127.0.0.1:8080/poll?payload=hello'
```

## Run polling client

```bash
python protocols/http/clients/poll_client.py --base-url http://127.0.0.1:8080 --payload tutorial --interval 1 --count 5
```

## Notes

- HTTP polling is easy to operate and widely supported.
- For high-frequency bidirectional realtime messaging, see the WebSocket track under `protocols/websocket/`.
