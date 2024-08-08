from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse


app = FastAPI()


HTML_STRING = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                data = JSON.stringify(input.value)
                ws.send(data)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@app.get("/")
async def get():
    return HTMLResponse(HTML_STRING)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint. once connected message can be sent
    back and forth with bi-directional paradigm.

    If server is stateful, we need to implement a session manager
    to manage session info which could hold websocket connection.
    """
    await websocket.accept() # socket connects when a client connects.
    await websocket.send_json({"status": "okie"}) # once connected send back status to client.
    # A listener like while loop rec/send json from/to client.
    while True:
        try:
            data = await websocket.receive_json()
            # app = your_app_or_model()
            # output = app.process(data)
            await websocket.send_json({
                "reversed_data": data[::-1],
                # "output": output,
                "status": "ok"
            })
        except ValueError as e:
            print(f"Error: {e}")
            await websocket.send_json({"status": "invalid JSON"})
            continue
        except WebSocketDisconnect:
            await websocket.send_json({"status":"socket closed."})
            # gracefully handle closing session here if server is stateful.
