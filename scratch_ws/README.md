# From-Scratch WebSocket Learning Track

This folder contains educational implementations to understand WebSocket internals.

## Files

- `helpers.py`: header parsing, accept-key generation, and minimal frame parsing/encoding.
- `handshake_server.py`: demonstrates only the HTTP Upgrade handshake (`101 Switching Protocols`).
- `frame_echo_server.py`: handshake + basic text frame echo/reverse loop.

## Run handshake demo

```bash
python scratch_ws/handshake_server.py
```

Then connect with any WebSocket client to `ws://127.0.0.1:8765` and inspect terminal output.

## Run frame echo demo

```bash
python scratch_ws/frame_echo_server.py
```

Then use browser console:

```js
const ws = new WebSocket("ws://127.0.0.1:8766");
ws.onmessage = (e) => console.log(e.data);
ws.onopen = () => ws.send("hello from browser");
```

Expected reply format:

- `echo-from-scratch: <reversed-message>`

## Important limitations (intentional)

This is intentionally minimal for teaching:
- text frames only
- no fragmentation handling
- no ping/pong implementation
- no production-grade error handling or security hardening

Use this to understand protocol mechanics, then compare with `server/listen.py` for framework abstraction.
