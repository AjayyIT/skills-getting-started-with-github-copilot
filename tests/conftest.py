"""Pytest configuration and fixtures for API tests"""
import pytest
from copy import deepcopy
from fastapi.testclient import TestClient
from src.app import app, activities

# Store original activities for reset between tests
ORIGINAL_ACTIVITIES = deepcopy(activities)


@pytest.fixture
def reset_activities():
    """
    Arrange: Reset activities to original state before each test.
    This fixture ensures test isolation by restoring the default activities state.
    """
    activities.clear()
    activities.update(deepcopy(ORIGINAL_ACTIVITIES))
    yield
    # Cleanup: Reset after test
    activities.clear()
    activities.update(deepcopy(ORIGINAL_ACTIVITIES))


@pytest.fixture
def client(reset_activities):
    """
    Arrange: Provide TestClient with fresh app state.
    The reset_activities fixture ensures activities are reset before each test.
    """
    return TestClient(app)
