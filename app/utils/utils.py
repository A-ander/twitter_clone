from fastapi import HTTPException, Request, status, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_session
from app.db.models.user_model import User


async def get_current_user(
        request: Request,
        session: AsyncSession = Depends(get_session)
) -> User:
    api_key = request.headers.get("Api-Key")
    user = await session.scalar(select(User).where(User.api_key == api_key))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return user
