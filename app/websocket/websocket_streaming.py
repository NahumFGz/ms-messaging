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
    Incluye un parámetro `streaming` para indicar si la respuesta aún se está generando.
    """
    # Simula una respuesta dividida en 5 partes
    for i in range(1, 6):
        await asyncio.sleep(1)  # Simula un retraso entre cada fragmento
        yield {
            "chat_uuid": chat_uuid,
            "message": f"Part {i}: {message}",
            "streaming": True,  # Indica que la respuesta aún se está generando
        }

    # Último mensaje para indicar que la respuesta ha finalizado
    yield {
        "chat_uuid": chat_uuid,
        "message": f"Final response: {message}",
        "streaming": False,  # Indica que la respuesta ha finalizado
    }


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

            # Variable para almacenar la respuesta completa
            full_response = ""

            # Conectar a la API de streaming y enviar cada fragmento al cliente
            async for chunk in connect_to_streaming_api(chat_uuid, message_content):
                await websocket.send_json(chunk)

                # Concatenar la respuesta completa
                full_response += chunk["message"] + " "

                # Si la respuesta ha finalizado, guardar el mensaje en la base de datos
                if not chunk["streaming"]:
                    # Crear el mensaje del sistema en la base de datos
                    system_message = MessageCreate(
                        chat_uuid=chunk["chat_uuid"],
                        sender_type="SYSTEM",
                        content=full_response.strip(),  # Elimina espacios adicionales
                    )
                    await create_message(system_message.model_dump(), session)

    except WebSocketDisconnect:
        print("WebSocket desconectado")
