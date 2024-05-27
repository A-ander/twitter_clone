import pytest
from httpx import AsyncClient
from fastapi import UploadFile
from app.db.models.user_model import User


@pytest.mark.asyncio
async def test_upload_media(client: AsyncClient, test_user: User, test_upload_file: UploadFile):
    response = await client.post(
        "/api/medias",
        files={"file": (test_upload_file.filename, test_upload_file.file, "image/png")},
        headers={"Api-Key": test_user.api_key}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["result"] is True
    assert "media_id" in data
