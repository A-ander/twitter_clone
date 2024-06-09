import logging
import os

import aiofiles
from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.media_model import Media
from app.db.models.user_model import User

logging.basicConfig(level='INFO')


async def upload_media_file(
    file: UploadFile,
    current_user: User,
    session: AsyncSession,
    media_storage_path: str = "/app/static/images"  # Make path configurable
):
    """Uploads a media file and saves it to the database.

    Args:
        file (UploadFile): The uploaded file.
        current_user (User): The current user.
        session (AsyncSession): The database session.
        media_storage_path (str, optional): The path to the media storage directory.
            Defaults to "/app/static/images".

    Returns:
        int: The ID of the newly created Media record.
    """

    file_name = f"{current_user.id}_{file.filename.replace(' ', '_')}"
    file_path = os.path.join(media_storage_path, file_name)
    logging.info(f"Saving file to path: {file_path}")

    async with aiofiles.open(file_path, "wb") as buffer:
        contents = await file.read()
        await buffer.write(contents)
        logging.info(f"File saved successfully: {file_path}")

    media = Media(file_path=file_path)
    session.add(media)
    await session.commit()
    await session.refresh(media)

    return media.id