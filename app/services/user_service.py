from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.user_model import User, user_followers


async def follow_user(
        current_user: User,
        user_id: int,
        session: AsyncSession
):
    user = await session.get(User, user_id)
    if user not in current_user.following:
        current_user.following.append(user)
        await session.commit()


async def unfollow_user(
        current_user: User,
        user_id: int,
        session: AsyncSession
):
    user = await session.get(User, user_id)
    if user in current_user.following:
        current_user.following.remove(user)
        await session.commit()


async def get_user_profile(current_user: User, session: AsyncSession):
    followers_query = await session.execute(
        select(User)
        .join(user_followers, User.id == user_followers.c.follower_id)
        .where(user_followers.c.followed_id == current_user.id)
    )
    followers = followers_query.scalars().all()
    followings_query = await session.execute(
        select(User)
        .join(user_followers, User.id == user_followers.c.followed_id)
        .where(user_followers.c.follower_id == current_user.id)
    )
    following = followings_query.scalars().all()
    return {
        "result": True,
        "user": {
            "id": current_user.id,
            "name": current_user.name,
            "followers": [
                {
                    "id": follower.id,
                    "name": follower.name
                } for follower in followers
            ],
            "following": [
                {
                    "id": following_user.id,
                    "name": following_user.name
                } for following_user in following
            ]
        }
    }


async def get_user_by_id(
        user_id: int,
        session: AsyncSession
):
    user = await session.get(User, user_id)
    return await get_user_profile(user, session)
