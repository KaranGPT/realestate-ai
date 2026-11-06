import os
from collections.abc import AsyncIterator

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from realestate_api import models  # noqa: F401
from realestate_api.core.database import Base, get_db
from realestate_api.main import app

TEST_DATABASE_URL = os.getenv(
    "REAI_TEST_DATABASE_URL",
    "postgresql+asyncpg://reai:reai_dev_password@localhost:5432/reai_test",
)


@pytest.fixture
async def client() -> AsyncIterator[AsyncClient]:
    assert TEST_DATABASE_URL.endswith("_test"), "Refusing to run tests on a non-test database"

    engine = create_async_engine(TEST_DATABASE_URL, poolclass=NullPool)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    session_factory = async_sessionmaker(engine, expire_on_commit=False)

    async def override_get_db() -> AsyncIterator[AsyncSession]:
        async with session_factory() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c

    app.dependency_overrides.clear()
    await engine.dispose()
