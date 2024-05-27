from typing import Optional

from pydantic import BaseModel

from app.api.schemas.result import Result
from app.api.schemas.user_schema import UserSchema


class TweetCreateSchema(BaseModel):
    tweet_data: str
    tweet_media_ids: list[int] = []

    class ConfigDict:
        from_attributes = True


class TweetLikesSchema(BaseModel):
    user_id: int
    name: str

    class ConfigDict:
        from_attributes = True


class TweetSchema(BaseModel):
    id: int
    content: str
    attachments: list[str]
    author: UserSchema
    likes: list[TweetLikesSchema]

    class ConfigDict:
        from_attributes = True


class TweetResponse(Result):
    tweets: list[TweetSchema]


class TweetResult(Result):
    tweet_id: int
