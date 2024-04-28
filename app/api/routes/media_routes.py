from fastapi import APIRouter, Depends, File, UploadFile

from app.services.media_service import upload_media_file
from app.utils.utils import get_current_user

router = APIRouter(prefix="/api/medias", tags=["Media"])


@router.post("/", status_code=201)
async def upload_media(
        file: UploadFile = File(...),
        current_user=Depends(get_current_user)
):
    media_id = await upload_media_file(file, current_user)
    return {"result": True, "media_id": media_id}
