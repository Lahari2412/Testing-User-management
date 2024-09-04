import pytest
from fastapi.testclient import TestClient
from main import app
from config.db import conn

client = TestClient(app)

@pytest.fixture(scope="module")
def setup_db():
    # Clean up before tests
    conn.local.members.drop()
    conn.local.counters.drop()  # Ensure counters collection is also clean
    yield
    # Clean up after tests
    conn.local.members.drop()
    conn.local.counters.drop()

def test_create_panel_member(setup_db):
    response = client.post(
        "/api/v1/member/",
        json={
            "name": "John Doe",
            "email": "johndoe@example.com",
            "mobile_number": 1234567890,
            "location": "Test Location"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["email"] == "johndoe@example.com"

def test_create_panel_member_conflict(setup_db):
    # First create a member
    client.post(
        "/api/v1/member/",
        json={
            "name": "Jane Doe",
            "email": "janedoe@example.com",
            "mobile_number": 9876543210,
            "location": "Another Location"
        }
    )

    # Try to create a member with the same email
    response = client.post(
        "/api/v1/member/",
        json={
            "name": "Jane Doe",
            "email": "janedoe@example.com",
            "mobile_number": 1122334455,
            "location": "Different Location"
        }
    )
    
    assert response.status_code == 422
    error_message = response.json().get("detail") or response.json().get("message")
    
    # Adjust assertion to handle the prefix
    expected_message = "Panel member with this email already exists"
    assert expected_message in error_message, f"Expected '{expected_message}' but got '{error_message}'"


def test_find_all_panel_members(setup_db):
    # Create a member first
    client.post(
        "/api/v1/member/",
        json={
            "name": "Jane Doe",
            "email": "janedoe@example.com",
            "mobile_number": 9876543210,
            "location": "Another Location"
        }
    )
    
    response = client.get("/api/v1/member/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)  # Expect a list of members
    assert len(data) > 0  # Check that there is at least one member

def test_get_panel_member(setup_db):
    # Create a member first
    create_response = client.post(
        "/api/v1/member/",
        json={
            "name": "Alice Smith",
            "email": "alicesmith@example.com",
            "mobile_number": 1122334455,
            "location": "Some Location"
        }
    )
    member_id = create_response.json()["id"]

    # Test getting the member
    response = client.get(f"/api/v1/member/{member_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "alicesmith@example.com"
    assert data["name"] == "Alice Smith"

def test_get_panel_member_not_found(setup_db):
    response = client.get("/api/v1/member/9999")  # Assuming ID 9999 does not exist
    assert response.status_code == 404
    assert response.json()["detail"] == "Panel Member with id 9999 not found"

def test_update_panel_member(setup_db):
    # Create a member first
    create_response = client.post(
        "/api/v1/member/",
        json={
            "name": "Bob Brown",
            "email": "bobbrown@example.com",
            "mobile_number": 2233445566,
            "location": "New Location"
        }
    )
    member_id = create_response.json()["id"]

    # Test updating the member
    update_response = client.put(
        f"/api/v1/member/{member_id}",
        json={
            "name": "Bob Updated",
            "location": "Updated Location"
        }
    )
    assert update_response.status_code == 200
    data = update_response.json()
    assert data["name"] == "Bob Updated"
    assert data["location"] == "Updated Location"

def test_update_panel_member_not_found(setup_db):
    update_response = client.put(
        "/api/v1/member/9999",  # Assuming ID 9999 does not exist
        json={
            "name": "Updated Name"
        }
    )
    assert update_response.status_code == 404
    assert update_response.json()["detail"] == "Panel Member with id 9999 not found"

def test_delete_panel_member(setup_db):
    # Create a member first
    create_response = client.post(
        "/api/v1/member/",
        json={
            "name": "Charlie Black",
            "email": "charlieblack@example.com",
            "mobile_number": 6677889900,
            "location": "Delete Location"
        }
    )
    member_id = create_response.json()["id"]

    # Test deleting the member
    delete_response = client.delete(f"/api/v1/member/{member_id}")
    assert delete_response.status_code == 200
    assert delete_response.json() == {"message": f"Panel Member with id {member_id} deleted successfully"}

    # Verify member is deleted
    get_response = client.get(f"/api/v1/member/{member_id}")
    assert get_response.status_code == 404
    assert get_response.json()["detail"] == f"Panel Member with id {member_id} not found"
