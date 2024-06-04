import pytest

from tests.conftest import true_response


@pytest.mark.asyncio
async def test_follow_user(client, add_user):
    header, _ = add_user
    user_id = 2
    response = await client.post(f"/api/users/{user_id}/follow", headers=header)
    true_response(response)


@pytest.mark.asyncio
async def test_unfollow_user(client, add_user):
    header, _ = add_user
    user_id = 2
    await client.post(f"/api/users/{user_id}/follow", headers=header)
    response = await client.delete(f"/api/users/{user_id}/follow", headers=header)
    true_response(response)


@pytest.mark.asyncio
async def test_get_my_profile(client, add_user):
    header, _ = add_user
    response = await client.get("/api/users/me", headers=header)
    true_response(response)
    assert "user" in response.json()
    user_data = response.json()["user"]
    assert "id" in user_data and "name" in user_data
    assert "followers" in user_data and "following" in user_data


@pytest.mark.asyncio
async def test_get_profile(client, add_user):
    header, _ = add_user
    user_id = 2
    response = await client.get(f"/api/users/{user_id}", headers=header)
    true_response(response)
    assert "user" in response.json()
    user_data = response.json()["user"]
    assert "id" in user_data and "name" in user_data
    assert "followers" in user_data and "following" in user_data
