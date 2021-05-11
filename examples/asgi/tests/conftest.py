import pytest
from app import app
from falcon.testing import TestClient


@pytest.fixture
@pytest.mark.asyncio
async def client():
    client = TestClient(app)
    async with client as conductor:
        yield conductor
