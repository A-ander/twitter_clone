from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.media_model import Media
from app.db.models.tweet_model import Tweet
from app.db.models.user_model import User


async def get_tweets_list_service(
        user: User,
        session: AsyncSession
) -> list[Tweet]:
    followed_users = user.following
    result = await session.execute(
        select(Tweet)
        .where(Tweet.author.in_(followed_users))
        .order_by(Tweet.created_at.desc())
    )
    tweets = result.scalars().all()
    return tweets


async def create_tweet_service(
        user: User,
        tweet_content: str,
        tweet_media_ids: list[int],
        session: AsyncSession
) -> Tweet:

    media_objects = [await session.get(Media, media_id) for media_id in tweet_media_ids]

    tweet = Tweet(
        content=tweet_content,
        author=user,
        media=media_objects
    )

    session.add(tweet)
    await session.commit()
    await session.refresh(tweet)

    return tweet
