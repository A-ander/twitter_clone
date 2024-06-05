import os

import pytest

from tests.conftest import true_response


@pytest.mark.asyncio
async def test_upload_media(client, add_user):
    header, user_id = add_user

    get_test_image = await client.get("https://cataas.com/cat")
    test_image = get_test_image.read()

    response = await client.post(
        '/api/medias', headers=header,
        files={'file': ('test_image.jpg', open(test_image, 'rb'), 'image/jpeg')}
    )
    true_response(response)
    assert 'media_id' in response.json() and response.json()['media_id'] == 1
