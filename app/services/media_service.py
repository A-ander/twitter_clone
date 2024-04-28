import os

from fastapi import UploadFile, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_session
from app.db.models.media_model import Media
from app.db.models.user_model import User


async def upload_media_file(
        file: UploadFile,
        current_user: User,
        session: AsyncSession = Depends(get_session)
):
    file_name = f"{current_user.id} {file.filename}"
    file_path = os.path.join("static", "upload", file_name)

    # Сохраняем файл на диск
    with open(file_path, "wb") as buffer:
        contents = await file.read()
        buffer.write(contents)

    # Создаем запись в базе данных
    media = Media(
        file=file_name,
        type=file.content_type,
        user=current_user
    )
    session.add(media)
    await session.commit()
    await session.refresh(media)

    return media.id
