import pytest
from httpx import AsyncClient

from app.db.models.tweet_model import Tweet
from app.db.models.user_model import User


@pytest.mark.asyncio
async def test_create_tweet(client: AsyncClient, test_user: User):
    response = await client.post(
        "/api/tweets",
        json={
            "tweet_data": "This is a test tweet",
            "tweet_media_ids": []
        },
        headers={"Api-Key": test_user.api_key}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["result"] is True
    assert "tweet_id" in data


@pytest.mark.asyncio
async def test_get_tweets(client: AsyncClient, test_user: User):
    response = await client.get(
        "/api/tweets",
        headers={"Api-Key": test_user.api_key}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["result"] is True
    assert len(data["tweets"]) > 0
    first_tweet = data["tweets"][0]
    assert "id" in first_tweet
    assert "content" in first_tweet
