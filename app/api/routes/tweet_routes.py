from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.result import Result
from app.api.schemas.tweet_schema import (
    TweetCreateSchema,
    TweetLikesSchema,
    TweetResponse,
    TweetResult,
    TweetSchema,
)
from app.db.database import get_session
from app.db.models.tweet_model import Tweet
from app.db.models.user_model import User
from app.services.tweet_service import (
    create_tweet_service,
    delete_tweet_service,
    like_tweet_service,
    unlike_tweet_service,
)
from app.services.tweet_service import get_tweets_list_service
from app.utils.utils import get_current_user

router = APIRouter(prefix='/api/tweets', tags=['tweets'])


@router.get('', response_model=TweetResponse)
async def get_tweets(
        user: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_session)
):
    """
    Retrieves a list of tweets for the current user.

    Args:
        user (User): The current user.
        session (AsyncSession): The database session.

    Returns:
        TweetResponse: A response containing a list of tweets.
    """
    tweets = await get_tweets_list_service(user=user, session=session)
    tweet_schemas = [
        TweetSchema(
            id=tweet.id,
            content=tweet.content,
            attachments=[media.file_path for media in tweet.media],
            author={
                "id": tweet.author.id,
                "name": tweet.author.name
            },
            likes=[
                TweetLikesSchema(
                    user_id=liked_user.id,
                    name=liked_user.name
                ) for liked_user in tweet.likes
            ]
        ) for tweet in tweets
    ]
    return TweetResponse(result=True, tweets=tweet_schemas)


@router.post('', response_model=TweetResult)
async def create_tweet(
        tweet_data: TweetCreateSchema,
        user: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_session)
):
    """
    Creates a new tweet for the current user.

    Args:
        tweet_data (TweetCreateSchema): The data for creating the tweet.
        user (User): The current user.
        session (AsyncSession): The database session.

    Returns:
        TweetResult: A response containing the ID of the created tweet.
    """
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
    """
    Deletes a tweet belonging to the current user.

    Args:
        tweet_id (int): The ID of the tweet to delete.
        user (User): The current user.
        session (AsyncSession): The database session.

    Returns:
        Result: A response indicating the success or failure of the operation.
    """
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
    """
    Allows the current user to like a tweet.

    Args:
        tweet_id (int): The ID of the tweet to like.
        user (User): The current user.
        session (AsyncSession): The database session.

    Returns:
        Result: A response indicating the success or failure of the operation.
    """
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
    """
    Allows the current user to unlike a tweet.

    Args:
        tweet_id (int): The ID of the tweet to unlike.
        user (User): The current user.
        session (AsyncSession): The database session.

    Returns:
        Result: A response indicating the success or failure of the operation.
    """
    tweet: Tweet | None = await session.get(Tweet, tweet_id)
    if not tweet:
        raise HTTPException(status_code=404, detail="Tweet not found")
    await unlike_tweet_service(tweet, user, session)
    return Result(result=True)
