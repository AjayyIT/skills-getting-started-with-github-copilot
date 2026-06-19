"""Tests for signup endpoint"""
import pytest


def test_signup_success(client):
    """Test successful signup for new student"""
    # Arrange: Fresh activity with known participants (via fixture)
    initial_response = client.get("/activities")
    initial_count = len(initial_response.json()["Chess Club"]["participants"])

    # Act: Register new student
    response = client.post("/activities/Chess Club/signup?email=newstudent@mergington.edu")

    # Assert: Verify success response
    assert response.status_code == 200
    assert "Signed up" in response.json()["message"]
    assert "newstudent@mergington.edu" in response.json()["message"]

    # Assert: Verify participant was added to activity
    activities_response = client.get("/activities")
    updated_count = len(activities_response.json()["Chess Club"]["participants"])
    assert updated_count == initial_count + 1
    assert "newstudent@mergington.edu" in activities_response.json()["Chess Club"]["participants"]


def test_signup_duplicate_rejected(client):
    """Test duplicate signup is rejected with 400 error"""
    # Arrange: Student already in Chess Club (default fixture state)

    # Act: Try to register same student again
    response = client.post("/activities/Chess Club/signup?email=michael@mergington.edu")

    # Assert: Verify rejection with correct error message
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_signup_invalid_activity(client):
    """Test signup for non-existent activity returns 404"""
    # Arrange: Invalid activity name ready

    # Act: Try to signup for fake activity
    response = client.post("/activities/Fake Club/signup?email=student@mergington.edu")

    # Assert: Verify 404 error
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_signup_multiple_students(client):
    """Test multiple different students can signup for same activity"""
    # Arrange: Fresh activity
    initial_count = len(client.get("/activities").json()["Programming Class"]["participants"])

    # Act: Register first new student
    response1 = client.post("/activities/Programming Class/signup?email=alice@mergington.edu")
    # Act: Register second new student
    response2 = client.post("/activities/Programming Class/signup?email=bob@mergington.edu")

    # Assert: Both signups succeeded
    assert response1.status_code == 200
    assert response2.status_code == 200

    # Assert: Both students are in the activity
    activities_response = client.get("/activities")
    participants = activities_response.json()["Programming Class"]["participants"]
    assert len(participants) == initial_count + 2
    assert "alice@mergington.edu" in participants
    assert "bob@mergington.edu" in participants
