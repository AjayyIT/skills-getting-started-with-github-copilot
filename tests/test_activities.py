"""Tests for GET endpoints (activities retrieval)"""
import pytest


def test_root_redirect(client):
    """Test GET / redirects to static/index.html"""
    # Arrange: Client is ready (via fixture)

    # Act: Call root endpoint
    response = client.get("/", follow_redirects=False)

    # Assert: Verify redirect
    assert response.status_code == 307
    assert "/static/index.html" in response.headers["location"]


def test_get_activities_returns_all_activities(client):
    """Test GET /activities returns all activities with correct structure"""
    # Arrange: Client with seeded activities (via fixture)

    # Act: Fetch all activities
    response = client.get("/activities")
    activities_data = response.json()

    # Assert: Verify structure and content
    assert response.status_code == 200
    assert isinstance(activities_data, dict)
    assert "Chess Club" in activities_data
    assert "Programming Class" in activities_data
    assert "Gym Class" in activities_data


def test_get_activities_includes_activity_details(client):
    """Test GET /activities returns complete activity details"""
    # Arrange: Client with seeded activities

    # Act: Fetch activities
    response = client.get("/activities")
    activities_data = response.json()
    chess_club = activities_data["Chess Club"]

    # Assert: Verify all required fields are present
    assert chess_club["description"] == "Learn strategies and compete in chess tournaments"
    assert chess_club["schedule"] == "Fridays, 3:30 PM - 5:00 PM"
    assert chess_club["max_participants"] == 12
    assert isinstance(chess_club["participants"], list)
    assert "michael@mergington.edu" in chess_club["participants"]
    assert "daniel@mergington.edu" in chess_club["participants"]


def test_get_activities_participant_count(client):
    """Test GET /activities includes correct participant counts"""
    # Arrange: Client with known participants

    # Act: Fetch activities
    response = client.get("/activities")
    activities_data = response.json()

    # Assert: Verify participant counts match
    assert len(activities_data["Chess Club"]["participants"]) == 2
    assert len(activities_data["Programming Class"]["participants"]) == 2
    assert len(activities_data["Gym Class"]["participants"]) == 2
