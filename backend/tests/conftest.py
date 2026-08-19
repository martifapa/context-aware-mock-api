"""Pytest configurations and shared fixtures"""

from collections.abc import AsyncGenerator
from unittest.mock import AsyncMock, patch

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.fixture(autouse=True)
def mock_redis():
    """Mock the Redis client for all tests to block real TCP/IP calls to the DDBB"""

    with (
        patch(
          "app.main.init_redis",
          new_callable=AsyncMock,
          create=True,
          ),
        patch(
          "app.main.close_redis",
          new_callable=AsyncMock,
          create=True,
          ),
        patch(
          "app.infrastructure.redis.redis_client",
          new_callable=AsyncMock,
          create=True,
          ),
    ):
        yield


@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    """Provides a thread-safe, async HTTPX client for testing"""

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac
