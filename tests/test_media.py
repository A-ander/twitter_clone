import pytest

from tests.conftest import true_response


@pytest.mark.asyncio
async def test_upload_media(client, add_media):
    """
    Tests the upload_media function.
    """
    header, user_id, media_file_name, media_file_content = add_media
    files = {'file': (media_file_name, media_file_content)}
    response = await client.post('/api/medias', headers=header, files=files)
    true_response(response)
    assert 'media_id' in response.json()
