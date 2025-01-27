from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class SenderTypeEnum(str, Enum):
    S = "S"  # System
    U = "U"  # Utils
    T = "T"  # Tool


class ChatBase(BaseModel):
    user_id: int


class ChatCreate(ChatBase):
    pass  # No incluye created_at ni updated_at


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
    chat_id: int
    sender_type: SenderTypeEnum
    content: str


class MessageCreate(MessageBase):
    pass  # No incluye timestamp


class MessageRead(MessageBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True


class MessageUpdate(BaseModel):
    chat_id: Optional[int] = None
    sender_type: Optional[str] = None
    content: Optional[str] = None

    class Config:
        from_attributes = True
