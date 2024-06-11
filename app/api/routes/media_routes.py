from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.media_schema import MediaSchema
from app.db.database import get_session
from app.services.media_service import upload_media_file
from app.utils.utils import get_current_user

router = APIRouter(prefix="/api/medias", tags=["media"])


@router.post('', response_model=MediaSchema)
async def upload_media(
        file: UploadFile = File(...),
        current_user=Depends(get_current_user),
        session: AsyncSession = Depends(get_session)
):
    """
    Uploads a media file and associates it with the current user.

    Args:
        file (UploadFile): The media file to be uploaded.
        current_user (User): The current user.
        session (AsyncSession): The database session.

    Returns:
        MediaSchema: A response containing the ID of the uploaded media.
    """
    media_id = await upload_media_file(file, current_user, session)
    return MediaSchema(result=True, media_id=media_id)
