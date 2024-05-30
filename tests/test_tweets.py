import pytest


@pytest.mark.asyncio
async def test_get_tweets(client, add_tweet):
    header, _ = add_tweet
    response = await client.get("/api/tweets", headers=header)
    assert response.status_code == 200
    data = response.json()
    assert "result" in data and data["result"] is True
    assert "tweets" in data
    tweets = data["tweets"]
    assert isinstance(tweets, list)


@pytest.mark.asyncio
async def test_create_tweet(client, add_user):
    header, _ = add_user
    tweet_data = {"tweet_data": "Test tweet", "tweet_media_ids": []}
    response = await client.post("/api/tweets", json=tweet_data, headers=header)
    assert response.status_code == 200
    data = response.json()
    assert "result" in data and data["result"] is True
    assert "tweet_id" in data
