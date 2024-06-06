import logging

import pytest

from tests.conftest import true_response

logging.basicConfig(level=logging.INFO)


@pytest.mark.asyncio
async def test_media(client, add_user):
    header, user_id = add_user

    with open("tests/test_image.jpg", "rb") as f:
        response = await client.post(
            '/api/medias',
            files={'file': ('test.jpg', f, 'image/jpeg')},
            headers=header
        )
        logging.info(response, '\n', header)

    true_response(response)
    assert 'media_id' in response.json() and response.json()['media_id'] == 1
