import socket

from scratch_ws.helpers import (
    compute_accept_key,
    make_ws_text_frame,
    parse_headers,
    read_ws_text_frame,
)


HOST = "127.0.0.1"
PORT = 8766


def handle_connection(conn: socket.socket) -> None:
    request = conn.recv(4096)
    headers = parse_headers(request)
    key = headers.get("sec-websocket-key")
    if not key:
        raise ValueError("Missing Sec-WebSocket-Key")

    accept_key = compute_accept_key(key)
    response = (
        "HTTP/1.1 101 Switching Protocols\r\n"
        "Upgrade: websocket\r\n"
        "Connection: Upgrade\r\n"
        f"Sec-WebSocket-Accept: {accept_key}\r\n\r\n"
    )
    conn.sendall(response.encode("utf-8"))

    while True:
        try:
            incoming = read_ws_text_frame(conn)
        except ConnectionAbortedError:
            break

        outgoing = f"echo-from-scratch: {incoming[::-1]}"
        conn.sendall(make_ws_text_frame(outgoing))


def main() -> None:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(5)

    print(f"Frame echo demo listening on ws://{HOST}:{PORT}")
    print("This server supports basic text frames only (educational demo).")

    while True:
        conn, addr = server.accept()
        print(f"Connected: {addr}")
        try:
            handle_connection(conn)
        except Exception as err:
            print(f"Connection error: {err}")
        finally:
            conn.close()
            print("Connection closed")


if __name__ == "__main__":
    main()
