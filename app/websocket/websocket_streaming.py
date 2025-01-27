import asyncio

from fastapi import Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import create_chat, create_message
from app.db import get_session
from app.schemas import MessageCreate


# Simula una API externa que devuelve datos en streaming
async def connect_to_streaming_api(chat_uuid: str, message: str):
    """
    Simula una API de streaming que devuelve datos en fragmentos.
    """
    # Simula una respuesta dividida en 5 partes
    for i in range(1, 6):
        await asyncio.sleep(1)  # Simula un retraso entre cada fragmento
        yield {"chat_uuid": chat_uuid, "message": f"Fragment {i}: {message}"}


# Endpoint de WebSocket para streaming
async def websocket_streaming_endpoint(websocket: WebSocket, session: AsyncSession = Depends(get_session)):
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

            # Conectar a la API de streaming y enviar cada fragmento al cliente
            async for chunk in connect_to_streaming_api(chat_uuid, message_content):
                await websocket.send_json(chunk)

                # Crear el mensaje del sistema en la base de datos (opcional)
                system_message = MessageCreate(
                    chat_uuid=chunk["chat_uuid"], sender_type="SYSTEM", content=chunk["message"]
                )
                await create_message(system_message.model_dump(), session)

    except WebSocketDisconnect:
        print("WebSocket desconectado")
