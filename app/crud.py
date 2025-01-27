from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models import Chat, Message


# CRUD para Chat
async def get_all_chats(session: AsyncSession):
    result = await session.execute(select(Chat))
    return result.scalars().all()


async def get_chat_by_id(chat_id: int, session: AsyncSession):
    result = await session.execute(select(Chat).where(Chat.id == chat_id))
    return result.scalar_one_or_none()


async def create_chat(chat_data: dict, session: AsyncSession):
    new_chat = Chat(**chat_data)
    session.add(new_chat)
    await session.commit()
    await session.refresh(new_chat)
    return new_chat


async def delete_chat(chat_id: int, session: AsyncSession):
    chat = await get_chat_by_id(chat_id, session)
    if not chat:
        raise NoResultFound(f"Chat with id {chat_id} not found.")
    await session.delete(chat)
    await session.commit()
    return {"message": "Chat deleted successfully"}


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
