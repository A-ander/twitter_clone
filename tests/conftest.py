import asyncio
import os
import sys
from typing import AsyncGenerator

import pytest_asyncio
from fastapi import UploadFile
from httpx import AsyncClient, ASGITransport
from sqlalchemy import NullPool
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
engine = create_async_engine(test_db, future=True, echo=True, poolclass=NullPool)
async_session = async_sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)


async def override_get_session():
    async with async_session() as session:
        yield session
    await session.close()

app.dependency_overrides[get_session] = override_get_session


@pytest_asyncio.fixture
async def init_db():
    """Fixture to create tables in test database"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def client(init_db) -> AsyncGenerator[AsyncClient, None]:
    """Fixture for HTTP client for requests"""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as async_client:
        yield async_client


@pytest_asyncio.fixture
async def test_session(init_db):
    async with AsyncSession(bind=engine) as session:
        yield session
    await session.close()


@pytest_asyncio.fixture
async def test_user(test_session: AsyncSession):
    user = User(name="Test User", api_key="test")
    test_session.add(user)
    await test_session.commit()
    await test_session.refresh(user)
    yield user
    await test_session.delete(user)
    await test_session.commit()


@pytest_asyncio.fixture
async def test_followee(test_session: AsyncSession, test_user: User):
    user2 = User(name="User2")
    test_session.add(user2)
    await test_session.commit()
    await test_session.refresh(user2)

    test_user.following.append(user2)
    await test_session.commit()

    yield user2

    await test_session.delete(user2)
    await test_session.commit()


@pytest_asyncio.fixture
async def test_tweet(test_session: AsyncSession, test_user: User):
    tweet = Tweet(content="Test Tweet", author=test_user)
    test_session.add(tweet)
    await test_session.commit()
    await test_session.refresh(tweet)
    yield tweet
    await test_session.delete(tweet)
    await test_session.commit()


@pytest_asyncio.fixture
async def test_media(test_session: AsyncSession):
    media = Media(file_path="/static/test_media.jpg")
    test_session.add(media)
    await test_session.commit()
    await test_session.refresh(media)
    yield media
    await test_session.delete(media)
    await test_session.commit()


@pytest_asyncio.fixture
async def test_upload_file() -> UploadFile:
    file_name = "test_file.png"
    file_data = b"test file data"
    return UploadFile(filename=file_name, file=file_data)


@pytest_asyncio.fixture
async def test_liked_tweet(test_session: AsyncSession, test_user: User):
    tweet = Tweet(content="Test Liked Tweet", author=test_user)
    tweet.likes.append(test_user)
    test_session.add(tweet)
    await test_session.commit()
    await test_session.refresh(tweet)
    yield tweet
    await test_session.delete(tweet)
    await test_session.commit()
