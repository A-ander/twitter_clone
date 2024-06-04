import pytest

from tests.conftest import true_response


@pytest.mark.asyncio
async def test_upload_media(client, add_media):
    header, media_id = add_media
    response = await client.post(f"/api/medias", headers=header)
    true_response(response)
    assert "media" in response.json()
    media_data = response.json()["media"]
    assert "id" in media_data and media_data["id"] == media_id
    assert "file_path" in media_data
