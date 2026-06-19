"""Tests for unregister endpoint"""
import pytest


def test_unregister_success(client):
    """Test successful unregister removes participant from activity"""
    # Arrange: Student is registered (default fixture state)
    initial_response = client.get("/activities")
    initial_count = len(initial_response.json()["Chess Club"]["participants"])
    assert "michael@mergington.edu" in initial_response.json()["Chess Club"]["participants"]

    # Act: Unregister participant
    response = client.post("/activities/Chess Club/unregister?email=michael@mergington.edu")

    # Assert: Verify success response
    assert response.status_code == 200
    assert "Unregistered" in response.json()["message"]
    assert "michael@mergington.edu" in response.json()["message"]

    # Assert: Verify participant was removed
    activities_response = client.get("/activities")
    updated_count = len(activities_response.json()["Chess Club"]["participants"])
    assert updated_count == initial_count - 1
    assert "michael@mergington.edu" not in activities_response.json()["Chess Club"]["participants"]


def test_unregister_not_participant(client):
    """Test unregister for non-existent participant returns 400"""
    # Arrange: Student not in activity

    # Act: Try to unregister non-participant
    response = client.post("/activities/Chess Club/unregister?email=nothere@mergington.edu")

    # Assert: Verify 400 error
    assert response.status_code == 400
    assert "Participant not found" in response.json()["detail"]


def test_unregister_invalid_activity(client):
    """Test unregister from non-existent activity returns 404"""
    # Arrange: Invalid activity name

    # Act: Try to unregister from fake activity
    response = client.post("/activities/Fake Club/unregister?email=student@mergington.edu")

    # Assert: Verify 404 error
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_unregister_then_resign_up(client):
    """Test student can unregister and then sign up again for same activity"""
    # Arrange: Student is registered
    assert "michael@mergington.edu" in client.get("/activities").json()["Chess Club"]["participants"]

    # Act: Unregister
    unregister_response = client.post("/activities/Chess Club/unregister?email=michael@mergington.edu")

    # Assert: Unregister successful
    assert unregister_response.status_code == 200
    assert "michael@mergington.edu" not in client.get("/activities").json()["Chess Club"]["participants"]

    # Act: Sign up again
    signup_response = client.post("/activities/Chess Club/signup?email=michael@mergington.edu")

    # Assert: Can sign up again successfully
    assert signup_response.status_code == 200
    assert "michael@mergington.edu" in client.get("/activities").json()["Chess Club"]["participants"]


def test_unregister_multiple_participants(client):
    """Test unregistering one participant doesn't affect others"""
    # Arrange: Activity with multiple participants
    initial_response = client.get("/activities")
    initial_participants = initial_response.json()["Chess Club"]["participants"].copy()
    assert len(initial_participants) == 2

    # Act: Unregister first participant
    response = client.post("/activities/Chess Club/unregister?email=michael@mergington.edu")

    # Assert: Only the unregistered participant was removed
    assert response.status_code == 200
    final_response = client.get("/activities")
    final_participants = final_response.json()["Chess Club"]["participants"]
    assert len(final_participants) == 1
    assert "daniel@mergington.edu" in final_participants
    assert "michael@mergington.edu" not in final_participants
