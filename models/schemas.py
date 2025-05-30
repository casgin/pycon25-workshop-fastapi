from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MessageBase(BaseModel):
    title: str
    category: str
    text: str

class MessageCreate(MessageBase):
    pass

class MessageUpdate(BaseModel):
    title: Optional[str] = None
    category: Optional[str] = None
    text: Optional[str] = None

class MessageResponse(MessageBase):
    id: int
    image: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    class Config:
        orm_mode = True