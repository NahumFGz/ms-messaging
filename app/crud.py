from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models import Chat, Message


# CRUD para Chat basado en uuid
async def get_all_chats(session: AsyncSession):
    result = await session.execute(select(Chat))
    return result.scalars().all()


async def get_chat_by_uuid(uuid: str, session: AsyncSession):
    result = await session.execute(select(Chat).where(Chat.uuid == uuid))
    return result.scalar_one_or_none()


async def create_chat(chat_data: dict, session: AsyncSession):
    new_chat = Chat(**chat_data)
    session.add(new_chat)
    await session.commit()
    await session.refresh(new_chat)
    return new_chat


async def delete_chat_by_uuid(uuid: str, session: AsyncSession):
    chat = await get_chat_by_uuid(uuid, session)
    if not chat:
        raise NoResultFound(f"Chat with uuid {uuid} not found.")
    await session.delete(chat)
    await session.commit()
    return {"message": "Chat deleted successfully"}


async def update_chat(uuid: str, chat_data: dict, session: AsyncSession):
    chat = await get_chat_by_uuid(uuid, session)
    if not chat:
        return None
    for key, value in chat_data.items():
        setattr(chat, key, value)
    await session.commit()
    await session.refresh(chat)
    return chat


async def get_messages_by_chat_uuid(uuid: str, session: AsyncSession):
    # Obtener el chat por uuid
    chat = await get_chat_by_uuid(uuid, session)
    if not chat:
        return None

    # Consultar los mensajes asociados al chat
    result = await session.execute(select(Message).where(Message.chat_id == chat.id))
    return result.scalars().all()


# CRUD para Message
async def get_all_messages(session: AsyncSession):
    result = await session.execute(select(Message))
    return result.scalars().all()


async def get_message_by_id(message_id: int, session: AsyncSession):
    result = await session.execute(select(Message).where(Message.id == message_id))
    return result.scalar_one_or_none()


async def create_message(message_data: dict, session: AsyncSession):
    new_message = Message(**message_data)
    session.add(new_message)
    await session.commit()
    await session.refresh(new_message)
    return new_message


async def delete_message(message_id: int, session: AsyncSession):
    message = await get_message_by_id(message_id, session)
    if not message:
        raise NoResultFound(f"Message with id {message_id} not found.")
    await session.delete(message)
    await session.commit()
    return {"message": "Message deleted successfully"}


async def update_message(message_id: int, message_data: dict, session: AsyncSession):
    message = await get_message_by_id(message_id, session)
    if not message:
        return None
    for key, value in message_data.items():
        setattr(message, key, value)
    await session.commit()
    await session.refresh(message)
    return message
