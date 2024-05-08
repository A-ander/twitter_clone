from typing import Union

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.tweet_schema import TweetSchema, TweetResponse
from app.db.database import get_session
from app.db.models.user_model import User
from app.services.tweet_service import create_tweet_service
from app.services.tweet_service import get_tweets_list_service
from app.utils.utils import get_current_user


router = APIRouter()


@router.get('/api/tweets', response_model=Union[list[TweetSchema], dict])
async def get_tweets(
        user: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_session)
) -> dict:
    try:
        tweets = await get_tweets_list_service(
            user=user,
            session=session
        )
    except Exception as e:
        return {
            "result": False,
            "error": e.__class__.__name__,
            "error_message": str(e)
        }

    return {
        "result": True,
        "tweets": [
            {
                "id": tweet.id,
                "content": tweet.content,
                "attachments": [f"/static/upload/{tweet.author.id} {media.file}" for media in tweet.media],
                # "attachments": [media.url for media in tweet.media],
                "author": {
                    "id": tweet.author.id,
                    "name": tweet.author.name
                },
                "likes": [
                    {
                        "user_id": user.id,
                        "name": user.name
                    } for user in tweet.likes
                ]
            } for tweet in tweets
        ]
    }


@router.post('/api/tweets', response_model=TweetResponse)
async def create_tweet(
        tweet_data: TweetSchema,
        user: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_session)
) -> dict:
    tweet_content = tweet_data.tweet_data
    tweet_media_ids = tweet_data.tweet_media_ids

    tweet = await create_tweet_service(
        user=user,
        tweet_content=tweet_content,
        tweet_media_ids=tweet_media_ids,
        session=session
    )
    return {"result": True, "tweet_id": tweet.id}
