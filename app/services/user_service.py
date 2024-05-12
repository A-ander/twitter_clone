from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

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
    user = await session.scalar(
        select(User)
        .options(joinedload(User.followers), joinedload(User.following))
        .where(User.id == current_user.id)
    )

    return {
        "result": True,
        "user": {
            "id": user.id,
            "name": user.name,
            "followers": [
                {
                    "id": follower.id,
                    "name": follower.name
                } for follower in user.followers
            ],
            "following": [
                {
                    "id": following_user.id,
                    "name": following_user.name
                } for following_user in user.following
            ]
        }
    }


async def get_user_by_id(
        user_id: int,
        session: AsyncSession
):
    user = await session.get(User, user_id)
    return await get_user_profile(user, session)
