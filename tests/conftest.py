import asyncio
import os
import sys
from typing import AsyncGenerator

import pytest_asyncio
from fastapi import UploadFile
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine
)

from app.core.config import TestSettings
from app.db.database import get_session, Base
from app.db.models.media_model import Media
from app.db.models.tweet_model import Tweet
from app.db.models.user_model import User
from app.main import app

test_db = TestSettings().db_url
engine = create_async_engine(test_db, future=True, echo=True)
async_session = async_sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)


async def override_get_session() -> AsyncSession:
    async with async_session() as session:
        yield session


app.dependency_overrides[get_session] = override_get_session()


@pytest_asyncio.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(autouse=True, scope="session")
async def init_db():
    """Fixture to create tables in test database"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="session")
async def client() -> AsyncGenerator[AsyncClient, None]:
    """Fixture for HTTP client for requests"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest_asyncio.fixture
async def test_user():
    async with override_get_session() as session:
        user = User(name="Test User", api_key="test")
        session.add(user)
        await session.commit()
        await session.refresh(user)
        yield user
        await session.delete(user)
        await session.commit()


@pytest_asyncio.fixture
async def test_followee(test_user):
    async with override_get_session() as session:
        user2 = User(name="User2")
        session.add(user2)
        await session.commit()
        await session.refresh(user2)

        test_user.following.append(user2)
        await session.commit()

        yield user2

        await session.delete(user2)
        await session.commit()


@pytest_asyncio.fixture
async def test_tweet(test_user):
    async with override_get_session() as session:
        tweet = Tweet(content="Test Tweet", author=test_user)
        session.add(tweet)
        await session.commit()
        await session.refresh(tweet)
        yield tweet
        await session.delete(tweet)
        await session.commit()


@pytest_asyncio.fixture
async def test_media():
    async with override_get_session() as session:
        media = Media(file_path="/static/test_media.jpg")
        session.add(media)
        await session.commit()
        await session.refresh(media)
        yield media
        await session.delete(media)
        await session.commit()


@pytest_asyncio.fixture
async def test_upload_file() -> UploadFile:
    file_name = "test_file.png"
    file_data = b"test file data"
    return UploadFile(filename=file_name, file=file_data)


@pytest_asyncio.fixture
async def test_liked_tweet(test_user):
    async with override_get_session() as session:
        tweet = Tweet(content="Test Liked Tweet", author=test_user)
        tweet.likes.append(test_user)
        session.add(tweet)
        await session.commit()
        await session.refresh(tweet)
        yield tweet
        await session.delete(tweet)
        await session.commit()
