"""Pytest configurations and shared fixtures"""

from collections.abc import AsyncGenerator
from unittest.mock import AsyncMock, patch

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.fixture(autouse=True)
def mock_redis():
    """Mock the Redis client for all tests to block real TCP/IP calls to the DDBB"""

    mock_client_instance = AsyncMock()

    with (
        patch(
          "app.main.pool",
          new_callable=AsyncMock
          ),
        patch(
          "app.infrastructure.redis.get_redis_client",
          return_value=mock_client_instance,
          ),
    ):
        yield mock_client_instance


@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    """Provides a thread-safe, async HTTPX client for testing"""

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac
