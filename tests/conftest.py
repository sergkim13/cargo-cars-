import asyncio

import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy_utils import create_database, database_exists

from config import DB_HOST, DB_PASS, DB_PORT, DB_USER, TEST_DB_NAME
from cars_app.cache.settings import redis_client
from cars_app.database.models import Base
from cars_app.database.settings import get_session
from cars_app.main import app

pytest_plugins = [
    'tests.fixtures.cargos',
    'tests.fixtures.locations',
    'tests.fixtures.cars',
]

# Test database fixtures
SQLALCHEMY_TEST_DATABASE_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{TEST_DB_NAME}'


# Test database fixtures
@pytest_asyncio.fixture(scope='session')
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope='session')
async def db_engine():
    engine = create_async_engine(SQLALCHEMY_TEST_DATABASE_URL)

    if not database_exists:
        create_database(engine.url)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    yield engine


@pytest_asyncio.fixture(scope='function')
async def session(db_engine):
    connection = await db_engine.connect()
    transaction = await connection.begin()
    session = AsyncSession(bind=connection)
    await redis_client.flushdb()

    yield session

    await redis_client.flushdb()
    await transaction.rollback()
    await connection.close()


@pytest_asyncio.fixture(scope='function')
async def client(session):
    app.dependency_overrides[get_session] = lambda: session

    async with AsyncClient(app=app, base_url='http://test') as client:
        yield client
