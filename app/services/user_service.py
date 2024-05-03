from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.user_model import User


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


async def get_user_profile(current_user: User):
    return {
        "result": True,
        "user": {
            "id": current_user.id,
            "name": current_user.name,
            "followers": [
                {
                    "id": follower.id,
                    "name": follower.name
                } for follower in current_user.followers
            ],
            "following": [
                {
                    "id": following.id,
                    "name": following.name
                } for following in current_user.following
            ]
        }
    }


async def get_user_by_id(
        user_id: int,
        session: AsyncSession
):
    user = await session.scalar(select(User).where(User.c.id == user_id))
    return await get_user_profile(user)
    