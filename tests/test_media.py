import logging
import os
import pytest
from tests.conftest import true_response

logging.basicConfig(level=logging.INFO)


@pytest.mark.asyncio
async def test_media(client, add_user, tmpdir):
    """
    Tests the upload_media function.
    """
    header, user_id = add_user
    media_storage_path = str(tmpdir.mkdir("media"))

    with open("tests/test_image.jpg", "rb") as f:
        response = await client.post(
            '/api/medias',
            files={'file': ('test.jpg', f, 'image/jpeg')},
            headers=header
        )
        logging.info(response)
        logging.info(header)

    true_response(response)
    assert 'media_id' in response.json() and response.json()['media_id'] == 1

    # Check if the file was saved correctly
    saved_file_path = os.path.join(media_storage_path, f"{user_id}_test.jpg")
    assert os.path.exists(saved_file_path)
