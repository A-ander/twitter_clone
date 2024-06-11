from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.result import Result
from app.api.schemas.user_schema import UserResponse
from app.db.database import get_session
from app.services.user_service import (
    get_user_by_id,
    get_user_profile,
    follow_user,
    unfollow_user,
)
from app.utils.utils import get_current_user

router = APIRouter(prefix='/api/users', tags=['users'])


@router.post('/{user_id}/follow', response_model=Result)
async def follow(
        user_id: int = Path(..., gt=0),
        current_user=Depends(get_current_user),
        session: AsyncSession = Depends(get_session)
):
    """
    Allows the current user to follow another user.

    Args:
        user_id (int): The ID of the user to follow.
        current_user (User): The current user.
        session (AsyncSession): The database session.

    Returns:
        Result: A response indicating the success or failure of the operation.
    """
    await follow_user(current_user, user_id, session)
    return Result(result=True)


@router.delete('/{user_id}/follow', response_model=Result)
async def unfollow(
        user_id: int = Path(..., gt=0),
        current_user=Depends(get_current_user),
        session: AsyncSession = Depends(get_session)
):
    """
    Allows the current user to unfollow another user.

    Args:
        user_id (int): The ID of the user to unfollow.
        current_user (User): The current user.
        session (AsyncSession): The database session.

    Returns:
        Result: A response indicating the success or failure of the operation.
    """
    await unfollow_user(current_user, user_id, session)
    return Result(result=True)


@router.get('/me', response_model=UserResponse)
async def get_my_profile(
        current_user=Depends(get_current_user),
        session=Depends(get_session)
):
    """
    Retrieves the profile data of the current user.

    Args:
        current_user (User): The current user.
        session (AsyncSession): The database session.

    Returns:
        UserResponse: A response containing the user's profile data.
    """
    user_data = await get_user_profile(current_user, session)
    return UserResponse(result=True, user=user_data)


@router.get('/{user_id}', response_model=UserResponse)
async def get_profile(
        user_id: int = Path(..., gt=0),
        session: AsyncSession = Depends(get_session)
):
    """
    Retrieves the profile data of a specific user.

    Args:
        user_id (int): The ID of the user whose profile is to be retrieved.
        session (AsyncSession): The database session.

    Returns:
        UserResponse: A response containing the user's profile data.
    """
    user_data = await get_user_by_id(user_id, session)
    return UserResponse(result=True, user=user_data)
