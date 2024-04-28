from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from .user_schema import UserSchema
from .media_schema import MediaSchema


class TweetSchema(BaseModel):
    content: str
    created_at: Optional[datetime]
    author: UserSchema
    media: list[MediaSchema] = []
    likes: list[UserSchema] = []

    class Config:
        from_attributes = True
