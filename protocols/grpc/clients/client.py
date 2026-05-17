"""gRPC client examples for unary, server-streaming, and bidi-streaming."""

from __future__ import annotations

import time

import grpc

from protocols.grpc.protos import chat_pb2, chat_pb2_grpc


def bidi_messages():
    for idx in range(3):
        yield chat_pb2.ChatMessage(room_id="r1", user_id="u1", text=f"hello-{idx}", ts=int(time.time()))
        time.sleep(0.2)


def main() -> None:
    with grpc.insecure_channel("127.0.0.1:50051") as channel:
        stub = chat_pb2_grpc.ChatServiceStub(channel)

        unary = stub.SendMessage(chat_pb2.SendMessageRequest(room_id="r1", user_id="u1", text="hi"))
        print("unary:", unary)

        print("server streaming:")
        for event in stub.StreamMessages(chat_pb2.StreamRequest(room_id="r1")):
            print("  ", event)

        print("bidi streaming:")
        for event in stub.ChatStream(bidi_messages()):
            print("  ", event)


if __name__ == "__main__":
    main()
