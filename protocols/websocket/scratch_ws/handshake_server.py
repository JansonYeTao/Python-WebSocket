import socket

from protocols.websocket.scratch_ws.helpers import compute_accept_key, parse_headers


HOST = "127.0.0.1"
PORT = 8765


def main() -> None:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(5)

    print(f"Handshake demo listening on {HOST}:{PORT}")
    print("Connect with a WebSocket client to observe the HTTP upgrade response.")

    conn, addr = server.accept()
    print(f"Accepted TCP connection from {addr}")

    request = conn.recv(4096)
    print("\n--- Raw HTTP Upgrade Request ---")
    print(request.decode("utf-8", errors="ignore"))

    headers = parse_headers(request)
    key = headers.get("sec-websocket-key")
    if not key:
        conn.close()
        raise ValueError("Missing Sec-WebSocket-Key")

    accept_key = compute_accept_key(key)
    response = (
        "HTTP/1.1 101 Switching Protocols\r\n"
        "Upgrade: websocket\r\n"
        "Connection: Upgrade\r\n"
        f"Sec-WebSocket-Accept: {accept_key}\r\n\r\n"
    )
    conn.sendall(response.encode("utf-8"))
    print("\n--- Sent 101 Switching Protocols ---")
    print(response)

    conn.close()
    server.close()


if __name__ == "__main__":
    main()
