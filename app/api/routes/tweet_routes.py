from fastapi import APIRouter, Depends

from app.api.schemas.tweet_schema import TweetSchema
from app.db.models.user_model import User
from app.services.tweet_service import create_tweet_service
from app.services.tweet_service import get_tweets_list_service
from app.utils.utils import get_current_user


router = APIRouter()


@router.get('/api/tweets', response_model=list[TweetSchema])
async def get_tweets(user: User = Depends(get_current_user)) -> dict:
    try:
        tweets = await get_tweets_list_service(user)
    except Exception as e:
        return {
            "result": False,
            "error": e.__class__.__name__,
            "error_message": str(e)
        }

    return {
        "result": True,
        "tweets": [
            {
                "id": tweet.id,
                "content": tweet.content,
                "attachments": [f"/static/upload/{tweet.author.id} {media.file}" for media in tweet.media],
                # "attachments": [media.url for media in tweet.media],
                "author": {
                    "id": tweet.author.id,
                    "name": tweet.author.name
                },
                "likes": [
                    {
                        "user_id": user.id,
                        "name": user.name
                    } for user in tweet.likes
                ]
            } for tweet in tweets
        ]
    }


@router.post('api/tweets', response_model=TweetSchema)
async def create_tweet(
        tweet_data: TweetSchema,
        user: User = Depends(get_current_user)
) -> dict:
    # data validation
    tweet_data = TweetSchema(**tweet_data.dict(exclude_unset=True))

    tweet = await create_tweet_service(
        user=user,
        tweet_data=tweet_data.dict()
    )
    return {"result": True, "tweet_id": tweet.id}
