from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.result import Result
from app.api.schemas.tweet_schema import TweetCreateSchema, TweetResponse, TweetResult
from app.db.database import get_session
from app.db.models.tweet_model import Tweet
from app.db.models.user_model import User
from app.services.tweet_service import (
    create_tweet_service,
    delete_tweet_service,
    like_tweet_service,
    unlike_tweet_service
)
from app.services.tweet_service import get_tweets_list_service
from app.utils.utils import get_current_user

router = APIRouter(prefix='/api/tweets', tags=['tweets'])


@router.get('', response_model=TweetResponse)
async def get_tweets(
        user: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_session)
):
    tweets = await get_tweets_list_service(user=user, session=session)
    return TweetResponse(result=True, tweets=tweets)


@router.post('', response_model=TweetResult)
async def create_tweet(
        tweet_data: TweetCreateSchema,
        user: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_session)
):
    tweet_content = tweet_data.tweet_data
    tweet_media_ids = tweet_data.tweet_media_ids

    tweet = await create_tweet_service(
        user=user,
        tweet_content=tweet_content,
        tweet_media_ids=tweet_media_ids,
        session=session
    )
    return TweetResult(result=True, tweet_id=tweet.id)


@router.delete('/{tweet_id}', response_model=Result)
async def delete_tweet(
        tweet_id: int,
        user: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_session),
):
    tweet: Tweet | None = await session.get(Tweet, tweet_id)
    if not tweet:
        raise HTTPException(status_code=404, detail="Tweet not found")
    if tweet.author_id != user.id:
        raise HTTPException(status_code=403, detail="You can only delete your own tweets")
    await delete_tweet_service(tweet, session)
    return Result(result=True)


@router.post('/{tweet_id}/likes', response_model=Result)
async def like_tweet(
        tweet_id: int,
        user: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_session),
):
    tweet: Tweet | None = await session.get(Tweet, tweet_id)
    if not tweet:
        raise HTTPException(status_code=404, detail="Tweet not found")
    await like_tweet_service(tweet, user, session)
    return Result(result=True)


@router.delete('/{tweet_id}/likes', response_model=Result)
async def unlike_tweet(
        tweet_id: int,
        user: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_session),
):
    tweet: Tweet | None = await session.get(Tweet, tweet_id)
    if not tweet:
        raise HTTPException(status_code=404, detail="Tweet not found")
    await unlike_tweet_service(tweet, user, session)
    return Result(result=True)
