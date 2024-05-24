import asyncio
from typing import AsyncGenerator

import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine
)

from app.core.config import TestSettings
from app.db.database import get_session, Base
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


# Fixture to create tables in test database
@pytest_asyncio.fixture(autouse=True, scope="session")
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


# Fixture for HTTP client for requests
@pytest_asyncio.fixture(scope="session")
async def client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        async with override_get_session() as _:
            yield ac
