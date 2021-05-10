import pytest
from app import app
from falcon.testing import TestClient


@pytest.fixture
def client():
    return TestClient(app)
