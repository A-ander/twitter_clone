import pytest
from httpx import AsyncClient

from app.db.models.user_model import User


@pytest.mark.asyncio
async def test_follow_user(client: AsyncClient, test_user: User, test_followee: User):
    response = await client.post(
        f"/api/users/{test_followee.id}/follow",
        headers={"Api-Key": test_user.api_key}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["result"] is True


@pytest.mark.asyncio
async def test_unfollow_user(client: AsyncClient, test_user: User, test_followee: User):
    # First, follow the test_followee
    response = await client.post(
        f"/api/users/{test_followee.id}/follow",
        headers={"Api-Key": test_user.api_key}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["result"] is True

    # Then, unfollow the test_followee
    response = await client.delete(
        f"/api/users/{test_followee.id}/follow",
        headers={"Api-Key": test_user.api_key}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["result"] is True
