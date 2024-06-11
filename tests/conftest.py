import logging
import os
import uuid
from typing import AsyncGenerator

import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import TestSettings
from app.db.database import get_session, Base
from app.db.models.media_model import Media
from app.db.models.tweet_model import Tweet
from app.db.models.user_model import User
from app.main import app

test_db = TestSettings().db_url
engine = create_async_engine(test_db, future=True, poolclass=NullPool)
async_session = async_sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession, autoflush=False
)


async def override_get_session():
    async with async_session() as session:
        yield session


app.dependency_overrides[get_session] = override_get_session


@pytest_asyncio.fixture(scope="session", autouse=True)
async def init_db():
    """Fixture to create tables in test database"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="session")
async def client(init_db) -> AsyncGenerator[AsyncClient, None]:
    """Fixture for HTTP client for requests"""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as async_client:
        yield async_client


@pytest_asyncio.fixture
async def test_session(init_db):
    async with AsyncSession(bind=engine) as session:
        yield session


def true_response(response):
    assert response.status_code == 200
    assert 'result' in response.json() and response.json()['result'] is True


@pytest_asyncio.fixture
async def add_user(test_session):
    """Fixture to add a new user to the database"""
    new_user = User(name='Test User', api_key=str(uuid.uuid4()))
    test_session.add(new_user)
    await test_session.commit()
    await test_session.refresh(new_user)
    header = {'api-key': new_user.api_key}
    yield header, new_user.id


@pytest_asyncio.fixture
async def add_tweet(test_session, add_user):
    """Fixture to add a new tweet to the database"""
    header, user_id = add_user
    new_tweet = Tweet(content='Test tweet', author_id=user_id)
    test_session.add(new_tweet)
    await test_session.commit()
    await test_session.refresh(new_tweet)
    yield header, new_tweet.id


@pytest_asyncio.fixture
async def add_media(test_session, add_user):
    """Fixture to add a new media to the database"""
    header, user_id = add_user
    media_file_name = "test_image.jpg"
    media_file_path = os.path.join(os.path.dirname(__file__), media_file_name)

    # Open a file and read its contents
    with open(media_file_path, 'rb') as f:
        media_file_content = f.read()

    new_media = Media(file_path=media_file_name)
    test_session.add(new_media)
    await test_session.commit()
    await test_session.refresh(new_media)
    yield header, new_media.id, media_file_name, media_file_content
