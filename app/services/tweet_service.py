import os

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
    """
    A service that retrieves a list of tweets for a given user.

    Args:
        user (User): The user for whom tweets are to be retrieved.
        session (AsyncSession): The database session.

    Returns:
        list[Tweet]: A list of Tweet objects.
    """
    # Explicitly load users that the current user is subscribed to
    current_user = await session.execute(
        select(User).options(selectinload(User.following)).where(User.id == user.id)
    )
    current_user = current_user.scalars().first()

    # Get the list of user IDs the current user is subscribed to
    followed_user_ids = [u.id for u in current_user.following]
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
    """
    A service that creates a new tweet for a given user.

    Args:
        user (User): The user creating the tweet.
        tweet_content (str): The content of the tweet.
        tweet_media_ids (list[int]): A list of media IDs associated with the tweet.
        session (AsyncSession): The database session.

    Returns:
        Tweet: The newly created Tweet object.
    """
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
    """
    A service that deletes a given tweet.

    Args:
        tweet (Tweet): The tweet to be deleted.
        session (AsyncSession): The database session.
    """
    # First, delete associated media files
    media_files = tweet.media
    for media in media_files:
        file_path = media.file_path
        os.remove(file_path)

    # Delete the tweet (cascades to likes and media associations)
    await session.delete(tweet)
    await session.commit()


async def like_tweet_service(tweet: Tweet, user: User, session: AsyncSession):
    """
    A service that allows a user to like a given tweet.

    Args:
        tweet (Tweet): The tweet to be liked.
        user (User): The user liking the tweet.
        session (AsyncSession): The database session.
    """
    tweet_query = await session.execute(
        select(Tweet)
        .options(selectinload(Tweet.likes))
        .where(Tweet.id == tweet.id)
    )
    tweet = tweet_query.scalar_one_or_none()

    if user not in tweet.likes:
        tweet.likes.append(user)
        await session.commit()
        await session.refresh(tweet)


async def unlike_tweet_service(tweet: Tweet, user: User, session: AsyncSession):
    """
    A service that allows a user to unlike a given tweet.

    Args:
        tweet (Tweet): The tweet to be unliked.
        user (User): The user unliking the tweet.
        session (AsyncSession): The database session.
    """
    tweet_query = await session.execute(
        select(Tweet)
        .options(selectinload(Tweet.likes))
        .where(Tweet.id == tweet.id)
    )
    tweet = tweet_query.scalar_one_or_none()

    if user in tweet.likes:
        tweet.likes.remove(user)
        await session.commit()
        await session.refresh(tweet)
