from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import (
    create_message,
    delete_message,
    get_all_messages,
    get_message_by_id,
    get_messages_by_chat_uuid,
    update_message,
)
from app.db import get_session
from app.schemas import MessageCreate, MessageRead, MessageUpdate

router = APIRouter()


@router.get("/", response_model=list[MessageRead])
async def read_messages(session: AsyncSession = Depends(get_session)):
    return await get_all_messages(session)


@router.get("/{chat_uuid}/", response_model=list[MessageRead])
async def read_messages_by_chat_uuid(chat_uuid: str, session: AsyncSession = Depends(get_session)):
    messages = await get_messages_by_chat_uuid(chat_uuid, session)
    if not messages:
        raise HTTPException(status_code=404, detail="No messages found for chat UUID")
    return messages


@router.post("/", response_model=MessageRead)
async def create_new_message(message: MessageCreate, session: AsyncSession = Depends(get_session)):
    return await create_message(message.model_dump(), session)


@router.delete("/{message_id}")
async def remove_message(message_id: int, session: AsyncSession = Depends(get_session)):
    try:
        return await delete_message(message_id, session)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.patch("/{message_id}", response_model=MessageRead)
async def update_message_details(
    message_id: int, message_update: MessageUpdate, session: AsyncSession = Depends(get_session)
):
    message = await update_message(message_id, message_update.model_dump(exclude_unset=True), session)
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    return message
