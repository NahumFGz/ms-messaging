import asyncio  # Para simular la demora
import uuid

from fastapi import Depends, FastAPI, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import create_chat, create_message
from app.db import get_session
from app.schemas import MessageCreate

app = FastAPI()


# Simula una función que conecta a otra API y devuelve una respuesta
async def connect_to_external_api(chat_uuid: str, message: str) -> dict:
    # Simula un retraso de 1 segundo
    await asyncio.sleep(1)
    return {"chat_uuid": chat_uuid, "message": f"{message} xxx"}


@app.websocket("/chat")
async def websocket_endpoint(websocket: WebSocket, session: AsyncSession = Depends(get_session)):
    await websocket.accept()
    try:
        while True:
            # Espera recibir un mensaje del cliente
            data = await websocket.receive_json()
            user_id = data.get("user_id")
            chat_uuid = data.get("chat_uuid")
            message_content = data.get("message", "")

            # Validación: el `user_id` debe estar presente
            if not user_id:
                await websocket.send_json({"error": "user_id is required"})
                continue

            # Si no se proporciona `chat_uuid`, se genera uno y se crea un nuevo chat
            if not chat_uuid:
                new_chat = await create_chat({"user_id": user_id}, session)
                chat_uuid = new_chat.uuid

            # Crear el mensaje del usuario en la base de datos
            user_message = MessageCreate(chat_uuid=chat_uuid, sender_type="USER", content=message_content)
            await create_message(user_message.model_dump(), session)

            # Simula la conexión a otra API para procesar el mensaje
            external_response = await connect_to_external_api(chat_uuid, message_content)

            # Crear el mensaje del sistema en la base de datos
            system_message = MessageCreate(
                chat_uuid=external_response["chat_uuid"], sender_type="SYSTEM", content=external_response["message"]
            )
            await create_message(system_message.model_dump(), session)

            # Retorna la respuesta al cliente
            await websocket.send_json(external_response)
    except WebSocketDisconnect:
        print("WebSocket desconectado")
