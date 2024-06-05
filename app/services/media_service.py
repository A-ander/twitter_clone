import os

import aiofiles
from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.media_model import Media
from app.db.models.user_model import User


async def upload_media_file(
        file: UploadFile,
        current_user: User,
        session: AsyncSession
):
    file_name = f"{current_user.id}_{file.filename.replace(' ', '_')}"
    file_path = os.path.join("/app/static/images", file_name)

    async with aiofiles.open(file_path, "wb") as buffer:
        contents = await file.read()
        await buffer.write(contents)

    media = Media(file_path=file_path)
    session.add(media)
    await session.commit()
    await session.refresh(media)

    return media.id
