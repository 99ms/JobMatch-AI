import pytest
from fastapi.testclient import TestClient
import os
import sys

# Ensure the app module is in the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.main import app

@pytest.fixture
def client():
    return TestClient(app)
