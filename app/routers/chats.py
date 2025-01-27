from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import (
    create_chat,
    delete_chat_by_uuid,
    get_all_chats,
    get_chat_by_uuid,
    update_chat,
)
from app.db import get_session
from app.schemas import ChatCreate, ChatRead, ChatUpdate

router = APIRouter()


@router.get("/", response_model=list[ChatRead])
async def read_chats(session: AsyncSession = Depends(get_session)):
    return await get_all_chats(session)


@router.get("/{uuid}", response_model=ChatRead)
async def read_chat(uuid: str, session: AsyncSession = Depends(get_session)):
    chat = await get_chat_by_uuid(uuid, session)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    return chat


@router.post("/", response_model=ChatRead)
async def create_new_chat(chat: ChatCreate, session: AsyncSession = Depends(get_session)):
    return await create_chat(chat.dict(), session)


@router.delete("/{uuid}")
async def remove_chat(uuid: str, session: AsyncSession = Depends(get_session)):
    try:
        return await delete_chat_by_uuid(uuid, session)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.patch("/{uuid}", response_model=ChatRead)
async def update_chat_details(uuid: str, chat_update: ChatUpdate, session: AsyncSession = Depends(get_session)):
    chat = await update_chat(uuid, chat_update.dict(exclude_unset=True), session)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    return chat
