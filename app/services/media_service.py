import logging
import os
import uuid

import aiofiles
from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.media_model import Media
from app.db.models.user_model import User

logging.basicConfig(level='INFO')


async def upload_media_file(
    file: UploadFile,
    current_user: User,
    session: AsyncSession
):
    """
    A service that uploads a media file and saves it to the database.

    Args:
        file (UploadFile): The uploaded file.
        current_user (User): The current user.
        session (AsyncSession): The database session.

    Returns:
        int: The ID of the newly created Media record.
    """

    unique_name = uuid.uuid4()
    file_name = str(unique_name) + str(current_user.id) + file.filename.replace(' ', '_')
    file_path = f'app/media/{file_name}'
    logging.info(f"Saving file to path: {file_path}")
    try:
        async with aiofiles.open(file_path, "wb") as buffer:
            contents = await file.read()
            await buffer.write(contents)
            logging.info(f"File saved successfully: {file_path}")
    except FileNotFoundError as e:
        logging.error(f"Error saving file: {e}")
        raise e

    media = Media(file_path=file_path)
    session.add(media)
    await session.commit()
    await session.refresh(media)

    return media.id
