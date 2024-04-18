from fastapi import HTTPException, Request, status
from sqlalchemy import select

from app.db.database import get_db
from app.db.models.user_model import User


async def get_current_user(request: Request) -> User:
    api_key = request.headers.get("Api-Key")
    async with get_db() as session:
        user = await session.scalar(select(User).where(User.api_key == api_key))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return user
