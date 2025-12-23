import pytest
from httpx import AsyncClient
from typing import AsyncGenerator

from src.main import app


@pytest.fixture
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
