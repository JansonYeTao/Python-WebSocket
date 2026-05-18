"""gRPC service implementation (requires generated *_pb2.py files)."""

from __future__ import annotations

import time
from concurrent import futures

import grpc

from protocols.grpc.protos import chat_pb2, chat_pb2_grpc


class ChatService(chat_pb2_grpc.ChatServiceServicer):
    def SendMessage(self, request, context):
        return chat_pb2.SendMessageReply(
            message_id=f"msg-{int(time.time() * 1000)}",
            server_ts=int(time.time()),
            status=f"ok:{request.room_id}:{request.user_id}",
        )

    def StreamMessages(self, request, context):
        for idx in range(5):
            yield chat_pb2.ChatMessage(
                room_id=request.room_id,
                user_id="server",
                text=f"stream-event-{idx}",
                ts=int(time.time()),
            )
            time.sleep(0.5)

    def ChatStream(self, request_iterator, context):
        for msg in request_iterator:
            yield chat_pb2.ChatMessage(
                room_id=msg.room_id,
                user_id="server-echo",
                text=f"echo:{msg.text}",
                ts=int(time.time()),
            )


def serve() -> None:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chat_pb2_grpc.add_ChatServiceServicer_to_server(ChatService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("gRPC server running on 0.0.0.0:50051")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
