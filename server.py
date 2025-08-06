import asyncio
import websockets
import http.server
import socketserver
import threading

HTTP_PORT = 3000
WS_PORT = 8765
STATIC_DIR = "public"
clients = set()

# --- WebSocket Server Logic ---
async def ws_handler(websocket, path):
    clients.add(websocket)
    try:
        async for message in websocket:
            tasks = [asyncio.create_task(client.send(message)) for client in clients if client != websocket]
            if tasks:
                await asyncio.wait(tasks)
    finally:
        clients.remove(websocket)

# --- HTTP Server Logic ---
def run_http_server():
    Handler = http.server.SimpleHTTPRequestHandler
    # We need to change directory into 'public' for the server to find the files
    class CustomHandler(Handler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=STATIC_DIR, **kwargs)

    with socketserver.TCPServer(("", HTTP_PORT), CustomHandler) as httpd:
        print(f"HTTP server serving '{STATIC_DIR}' at port {HTTP_PORT}")
        httpd.serve_forever()

# --- Main async function for WebSocket ---
async def main_ws():
    async with websockets.serve(ws_handler, "0.0.0.0", WS_PORT):
        print(f"WebSocket server started on port {WS_PORT}")
        await asyncio.Future()  # run forever

# --- Main execution block ---
if __name__ == "__main__":
    # Run the HTTP server in a separate thread
    http_thread = threading.Thread(target=run_http_server)
    http_thread.daemon = True
    http_thread.start()

    # Run the WebSocket server using asyncio.run()
    try:
        asyncio.run(main_ws())
    except KeyboardInterrupt:
        print("Servers shutting down.")
