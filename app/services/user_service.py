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


async def get_user_profile(current_user: User, session: AsyncSession):
    user = await session.get(User, current_user.id)

    followers_result = await session.execute(user.followers.select())
    following_result = await session.execute(user.following.select())

    # Retrieve users from the results
    followers = followers_result.scalars().all()
    following = following_result.scalars().all()

    return {
        "result": True,
        "user": {
            "id": user.id,
            "name": user.name,
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
