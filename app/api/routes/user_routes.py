from fastapi import APIRouter, Depends, Path

from app.services.user_service import (
    follow_user,
    unfollow_user,
    get_user_profile,
    get_user_by_id
)
from app.utils.utils import get_current_user

router = APIRouter(prefix='/api/users', tags=['Users'])


@router.post('/{user_id}/follow', status_code=200)
async def follow(
        user_id: int = Path(..., gt=0),
        current_user=Depends(get_current_user)
):
    await follow_user(current_user, user_id)
    return {'result': True}


@router.delete('/{user_id}/follow', status_code=200)
async def unfollow(
        user_id: int = Path(..., gt=0),
        current_user=Depends(get_current_user)
):
    await unfollow_user(current_user, user_id)
    return {'result': True}


@router.get('/me', response_model=dict)
async def get_my_profile(current_user=Depends(get_current_user)):
    return await get_user_profile(current_user)


@router.get('/{user_id}', response_model=dict)
async def get_profile(user_id: int = Path(..., gt=0)):
    return await get_user_by_id(user_id)
