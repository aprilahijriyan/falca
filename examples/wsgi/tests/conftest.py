import pytest
from app import app

from falca.testing import TestClient


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def settings():
    settings = app.settings
    settings.clear()
    return settings
