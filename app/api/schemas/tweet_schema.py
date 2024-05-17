from typing import Optional

from pydantic import BaseModel

from app.api.schemas.result import Result
from app.api.schemas.user_schema import UserSchema


class TweetCreateSchema(BaseModel):
    tweet_data: str
    tweet_media_ids: Optional[list[int]] = []

    class Config:
        from_attributes = True


class TweetSchema(BaseModel):
    id: int
    content: str
    attachments: Optional[list[str]] = []
    author: UserSchema
    likes: list[UserSchema]

    class Config:
        from_attributes = True


class TweetResponse(Result):
    tweets: list[TweetSchema]


class TweetResult(Result):
    tweet_id: int
