from pydantic import BaseModel


class TweetSchema(BaseModel):
    tweet_data: str
    tweet_media_ids: list[int] = []

    class Config:
        from_attributes = True


class TweetResponse(BaseModel):
    result: bool
    tweet_id: int

    class Config:
        from_attributes = True
