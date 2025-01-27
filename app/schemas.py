from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class ChatBase(BaseModel):
    user_id: int


class ChatCreate(ChatBase):
    pass


class ChatRead(ChatBase):
    id: int
    uuid: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ChatUpdate(BaseModel):
    user_id: Optional[int] = None

    class Config:
        from_attributes = True


class MessageBase(BaseModel):
    chat_uuid: str
    sender_type: str
    content: str


class MessageCreate(MessageBase):
    pass


class MessageRead(MessageBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True


class MessageUpdate(BaseModel):
    chat_uuid: Optional[str] = None
    sender_type: Optional[str] = None
    content: Optional[str] = None

    class Config:
        from_attributes = True
