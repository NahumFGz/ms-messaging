from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import create_chat, delete_chat, get_all_chats, get_chat_by_id
from app.db import get_session
from app.schemas import ChatCreate, ChatRead

router = APIRouter()


@router.get("/", response_model=list[ChatRead])
async def read_chats(session: AsyncSession = Depends(get_session)):
    return await get_all_chats(session)


@router.get("/{chat_id}", response_model=ChatRead)
async def read_chat(chat_id: int, session: AsyncSession = Depends(get_session)):
    chat = await get_chat_by_id(chat_id, session)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    return chat


@router.post("/", response_model=ChatRead)
async def create_new_chat(chat: ChatCreate, session: AsyncSession = Depends(get_session)):
    return await create_chat(chat.dict(), session)


@router.delete("/{chat_id}")
async def remove_chat(chat_id: int, session: AsyncSession = Depends(get_session)):
    try:
        return await delete_chat(chat_id, session)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
