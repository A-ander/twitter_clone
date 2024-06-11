from fastapi import Depends, HTTPException, status, Security
from fastapi.security import APIKeyHeader
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_session
from app.db.models.user_model import User

api_key_header = APIKeyHeader(name='Api-Key', auto_error=False)


async def get_current_user(
    api_key: str = Security(api_key_header),
    session: AsyncSession = Depends(get_session)
) -> User | None:
    """
    Retrieves the current user based on the provided API key.

    Args:
        api_key (str): The API key of the current user.
        session (AsyncSession): The database session.

    Returns:
        User | None: The current user object if found, None otherwise.
    """
    user = await session.scalar(select(User).where(User.api_key == api_key))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API Key")
    return user
