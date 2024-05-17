from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.user_schema import UserFullSchema, UserSchema
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


async def get_user_profile(chosen_user: User, session: AsyncSession):
    user = await session.get(User, chosen_user.id)

    followers_result = await session.execute(user.followers.select())
    following_result = await session.execute(user.following.select())

    # Retrieve users from the results
    followers = followers_result.scalars().all()
    following = following_result.scalars().all()

    return UserFullSchema(
        id=user.id,
        name=user.name,
        followers=[UserSchema(id=follower.id, name=follower.name) for follower in followers],
        following=[UserSchema(id=following_user.id, name=following_user.name) for following_user in following]
    )


async def get_user_by_id(
        user_id: int,
        session: AsyncSession
):
    user: User | None = await session.get(User, user_id)
    return await get_user_profile(user, session)


# async def follow_user_service(
#         current_user: User,
#         followed_user: User,
#         session: AsyncSession,
# ):
#     if followed_user not in current_user.following:
#         current_user.following.append(followed_user)
#         await session.commit()
#
#
# async def unfollow_user_service(
#         current_user: User,
#         followed_user: User,
#         session: AsyncSession,
# ):
#     if followed_user in current_user.following:
#         current_user.following.remove(followed_user)
#         await session.commit()
