import logging
import os

import aiofiles
from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.media_model import Media
from app.db.models.user_model import User

logger = logging.getLogger(__name__)


async def upload_media_file(
        file: UploadFile,
        current_user: User,
        session: AsyncSession
):
    file_name = f"{current_user.id}_{file.filename.replace(' ', '_')}"
    file_path = os.path.join("/app/static/images", file_name)
    logger.info(f"Saving file to path: {file_path}")

    try:
        async with aiofiles.open(file_path, "wb") as buffer:
            contents = await file.read()
            await buffer.write(contents)
            logger.info(f"File saved successfully: {file_path}")
    except Exception as e:
        logger.error(f"Error saving file: {e}")

    media = Media(file_path=file_path)
    session.add(media)
    await session.commit()
    await session.refresh(media)

    return media.id
