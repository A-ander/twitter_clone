from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.models.media_model import Media
from app.db.models.tweet_model import Tweet
from app.db.models.user_model import User


async def get_tweets_list_service(
        user: User,
        session: AsyncSession
) -> list[Tweet]:
    following_result = await session.execute(user.following.select())
    followed_user_ids = [u.id for u in following_result.scalars()]
    # Add the current user's ID, so they can see their tweets
    followed_user_ids.append(user.id)

    result = await session.scalars(
        select(Tweet)
        .options(selectinload(Tweet.author))
        .where(Tweet.author_id.in_(followed_user_ids))
        .order_by(Tweet.created_at.desc())
    )
    tweets = result.all()
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


async def delete_tweet_service(tweet: Tweet, session: AsyncSession):
    await session.delete(tweet)
    await session.commit()


async def like_tweet_service(tweet: Tweet, user: User, session: AsyncSession):
    tweet_query = await session.execute(
        select(Tweet)
        .options(selectinload(Tweet.likes))
        .where(Tweet.id == tweet.id)
    )
    tweet = tweet_query.scalar_one_or_none()

    if user not in tweet.likes:
        tweet.likes.append(user)
        await session.commit()


async def unlike_tweet_service(tweet: Tweet, user: User, session: AsyncSession):
    tweet_query = await session.execute(
        select(Tweet)
        .options(selectinload(Tweet.likes))
        .where(Tweet.id == tweet.id)
    )
    tweet = tweet_query.scalar_one_or_none()

    if user in tweet.likes:
        tweet.likes.remove(user)
        await session.commit()
