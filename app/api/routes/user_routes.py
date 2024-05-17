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
    # follow_user_service,
    # unfollow_user_service,
)
from app.utils.utils import get_current_user

router = APIRouter(prefix='/api/users', tags=['users'])


@router.post('/{user_id}/follow', response_model=Result)
async def follow(
        user_id: int = Path(..., gt=0),
        current_user=Depends(get_current_user),
        session: AsyncSession = Depends(get_session)
):
    await follow_user(current_user, user_id, session)
    return Result(result=True)


@router.delete('/{user_id}/follow', response_model=Result)
async def unfollow(
        user_id: int = Path(..., gt=0),
        current_user=Depends(get_current_user),
        session: AsyncSession = Depends(get_session)
):
    await unfollow_user(current_user, user_id, session)
    return Result(result=True)


@router.get('/me', response_model=UserResponse)
async def get_my_profile(
        current_user=Depends(get_current_user),
        session=Depends(get_session)
):
    user_data = await get_user_profile(current_user, session)
    return UserResponse(result=True, user=user_data)


@router.get('/{user_id}', response_model=UserResponse)
async def get_profile(
        user_id: int = Path(..., gt=0),
        session: AsyncSession = Depends(get_session)
):
    user_data = await get_user_by_id(user_id, session)
    return UserResponse(result=True, user=user_data)


# @router.post('/{user_id}/follow', response_model=dict)
# async def follow_user(
#         user_id: int,
#         user: User = Depends(get_current_user),
#         session: AsyncSession = Depends(get_session),
# ):
#     followed_user: User | None = await session.get(User, user_id)
#     if not followed_user:
#         raise HTTPException(status_code=404, detail="User not found")
#     await follow_user_service(user, followed_user, session)
#     return {"result": True}
#
#
# @router.delete('/{user_id}/follow', response_model=dict)
# async def unfollow_user(
#         user_id: int,
#         user: User = Depends(get_current_user),
#         session: AsyncSession = Depends(get_session),
# ):
#     followed_user: User | None = await session.get(User, user_id)
#     if not followed_user:
#         raise HTTPException(status_code=404, detail="User not found")
#     await unfollow_user_service(user, followed_user, session)
#     return {"result": True}
