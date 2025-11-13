import pytest
from httpx import AsyncClient

from src.main import app


@pytest.fixture
async def ac() -> AsyncClient:
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
