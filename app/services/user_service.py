from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.api.schemas.user_schema import UserFullSchema, UserSchema
from app.db.models.user_model import User


async def follow_user(
        current_user: User,
        user_id: int,
        session: AsyncSession
):
    """
    A service that allows a user to follow another user.

    Args:
        current_user (User): The user who wants to follow another user.
        user_id (int): The ID of the user to be followed.
        session (AsyncSession): The database session.
    """
    user = await session.get(User, user_id)
    current_user = await session.execute(
        select(User).options(selectinload(User.following)).where(User.id == current_user.id)
    )
    current_user = current_user.scalars().first()

    if user not in current_user.following:
        current_user.following.append(user)
        await session.commit()


async def unfollow_user(
        current_user: User,
        user_id: int,
        session: AsyncSession
):
    """
    A service that allows a user to unfollow another user.

    Args:
        current_user (User): The user who wants to unfollow another user.
        user_id (int): The ID of the user to be unfollowed.
        session (AsyncSession): The database session.
    """
    user = await session.get(User, user_id)
    current_user = await session.execute(
        select(User).options(selectinload(User.following)).where(User.id == current_user.id)
    )
    current_user = current_user.scalars().first()

    if user in current_user.following:
        current_user.following.remove(user)
        await session.commit()


async def get_user_profile(chosen_user: User, session: AsyncSession):
    """
    A service that retrieves the profile data of a given user.

    Args:
        chosen_user (User): The user whose profile data is to be retrieved.
        session (AsyncSession): The database session.

    Returns:
        UserFullSchema: The profile data of the given user.
    """
    user = await session.execute(
        select(User)
        .options(selectinload(User.followers), selectinload(User.following))
        .where(User.id == chosen_user.id)
    )
    user = user.scalars().first()

    followers = user.followers
    following = user.following

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
    """
    A service that retrieves a user object by ID.

    Args:
        user_id (int): The ID of the user to be retrieved.
        session (AsyncSession): The database session.

    Returns:
        UserFullSchema: The profile data of the retrieved user.
    """
    user: User | None = await session.get(User, user_id)
    return await get_user_profile(user, session)
