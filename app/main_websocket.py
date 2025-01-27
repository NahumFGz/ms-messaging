from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from app.websocket.websocket import websocket_endpoint

# Crear la aplicación FastAPI para el WebSocket
app_websocket = FastAPI()

# Registrar el endpoint de WebSocket
app_websocket.websocket("/chat")(websocket_endpoint)

# # Ejecutar el WebSocket en el puerto 8001
# if __name__ == "__main__":
#     import uvicorn

#     uvicorn.run(app_websocket, host="0.0.0.0", port=8001)
