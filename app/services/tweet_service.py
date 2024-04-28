from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_session
from app.db.models.media_model import Media
from app.db.models.tweet_model import Tweet
from app.db.models.user_model import User


async def get_tweets_list_service(
        user: User,
        session: AsyncSession = Depends(get_session)
) -> list[Tweet]:
    followed_users = user.following
    tweets = await session.scalars(
        select(Tweet)
        .where(Tweet.author.in_(followed_users))
        .order_by(Tweet.created_at.desc())
    ).all()  # Убрать all()?
    return tweets


async def create_tweet_service(
        user: User,
        tweet_data: dict,
        session: AsyncSession = Depends(get_session)
) -> Tweet.id:
    tweet_content = tweet_data.get('tweet_data')
    tweet_media_ids = tweet_data.get('tweet_media_ids', [])

    # Получаем объекты Media из базы данных по их идентификаторам
    media_objects = [session.get(Media, media_id) for media_id in tweet_media_ids]

    tweet = Tweet(
        content=tweet_content,
        author=user,
        media=media_objects
    )

    session.add(tweet)
    await session.commit()
    await session.refresh(tweet)

    return tweet.id
