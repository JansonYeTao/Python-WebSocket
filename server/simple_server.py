from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint. once connected message can be sent
    back and forth with bi-directional paradigm.

    If server is stateful, we can implement a session manager
    to manage session info which could hold websocket connection.
    """
    await websocket.accept() # socket connects when a client connects.
    await websocket.send_json({"status": "ok"}) # once connected send back status to client.
    # A listener like while loop rec/send json from/to client.
    while True:
        try:
            data = await websocket.receive_json()
            # app = your_app_or_model()
            # output = app.process(data)
            await websocket.send_json({
                "data": data,
                # "output": output,
                "status": "ok"
            })
        except ValueError:
            await websocket.send_error("invalid JSON")
            continue
        except WebSocketDisconnect:
            await websocket.send_json({"status":"socket closed."})
            # gracefully handle closing session here if server is stateful.
