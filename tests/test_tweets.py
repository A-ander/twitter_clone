import pytest

from tests.conftest import true_response


@pytest.mark.asyncio
async def test_get_tweets(client, add_tweet):
    header, _ = add_tweet
    response = await client.get("/api/tweets", headers=header)
    true_response(response)
    assert "tweets" in response.json()
    tweets = response.json()["tweets"]
    assert isinstance(tweets, list)


@pytest.mark.asyncio
async def test_create_tweet(client, add_user):
    header, _ = add_user
    tweet_data = {"tweet_data": "Test tweet", "tweet_media_ids": []}
    response = await client.post("/api/tweets", json=tweet_data, headers=header)
    true_response(response)
    assert "tweet_id" in response.json()


@pytest.mark.asyncio
async def test_delete_tweet(client, add_tweet):
    header, tweet_id = add_tweet
    response = await client.delete(f"/api/tweets/{tweet_id}", headers=header)
    true_response(response)


@pytest.mark.asyncio
async def test_like_tweet(client, add_tweet):
    header, _ = add_tweet
    tweet_id = 2
    response = await client.post(f"/api/tweets/{tweet_id}/likes", headers=header)
    true_response(response)


@pytest.mark.asyncio
async def test_unlike_tweet(client, add_tweet):
    header, _ = add_tweet
    tweet_id = 2
    await client.post(f"/api/tweets/{tweet_id}/likes", headers=header)
    response = await client.delete(f"/api/tweets/{tweet_id}/likes", headers=header)
    true_response(response)
