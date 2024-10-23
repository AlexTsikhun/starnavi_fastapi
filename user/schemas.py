from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class TokenData(BaseModel):
    id: Optional[str] = None


class User(BaseModel):
    email: EmailStr
    created_at: datetime
    auto_reply_enabled: bool
    reply_delay: int

    class Config:
        orm_mode = True


class AutoReplyToggleResponse(BaseModel):
    previous_state: bool
    new_state: bool
    message: str

    class Config:
        orm_mode = True


class UpdateReplyDelayRequest(BaseModel):
    delay: int
