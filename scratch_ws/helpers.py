import base64
import hashlib
import struct
from typing import Tuple


WS_GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"


def compute_accept_key(sec_websocket_key: str) -> str:
    raw = (sec_websocket_key + WS_GUID).encode("utf-8")
    digest = hashlib.sha1(raw).digest()
    return base64.b64encode(digest).decode("utf-8")


def parse_headers(http_request: bytes) -> dict[str, str]:
    lines = http_request.decode("utf-8", errors="ignore").split("\r\n")
    headers: dict[str, str] = {}
    for line in lines[1:]:
        if not line or ":" not in line:
            continue
        key, value = line.split(":", 1)
        headers[key.strip().lower()] = value.strip()
    return headers


def read_exact(sock, n: int) -> bytes:
    data = b""
    while len(data) < n:
        chunk = sock.recv(n - len(data))
        if not chunk:
            raise ConnectionError("Socket closed while reading")
        data += chunk
    return data


def read_ws_text_frame(sock) -> str:
    first2 = read_exact(sock, 2)
    b1, b2 = first2[0], first2[1]

    opcode = b1 & 0x0F
    masked = (b2 & 0x80) >> 7
    payload_len = b2 & 0x7F

    if opcode == 0x8:
        raise ConnectionAbortedError("Client sent close frame")

    if opcode != 0x1:
        raise ValueError(f"Only text frames are supported in this demo. opcode={opcode}")

    if payload_len == 126:
        payload_len = struct.unpack("!H", read_exact(sock, 2))[0]
    elif payload_len == 127:
        payload_len = struct.unpack("!Q", read_exact(sock, 8))[0]

    if masked != 1:
        raise ValueError("Client frames must be masked")

    masking_key = read_exact(sock, 4)
    masked_payload = read_exact(sock, payload_len)

    payload = bytes(b ^ masking_key[i % 4] for i, b in enumerate(masked_payload))
    return payload.decode("utf-8", errors="replace")


def make_ws_text_frame(message: str) -> bytes:
    payload = message.encode("utf-8")
    payload_len = len(payload)

    header = bytearray()
    header.append(0x81)

    if payload_len <= 125:
        header.append(payload_len)
    elif payload_len <= 65535:
        header.append(126)
        header.extend(struct.pack("!H", payload_len))
    else:
        header.append(127)
        header.extend(struct.pack("!Q", payload_len))

    return bytes(header) + payload
