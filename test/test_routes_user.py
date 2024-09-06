import pytest
from fastapi.testclient import TestClient
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import app
from config.db import conn

client = TestClient(app)

@pytest.fixture(scope="module")
def setup_db():
    # Ensure the user collection is empty before tests
    conn.local.user.drop()
    conn.local.counters.drop()  # Ensure counters collection is also empty for sequence values
    yield
    conn.local.user.drop()
    conn.local.counters.drop()

def test_create_user(setup_db):
    response = client.post(
        "/api/v1/user/",
        json={
            "name": "John Doe",
            "email": "johndoe@example.com",
            "mobile_number": 1234567890,
            "location": "Test Location",
            "password": "Password123!"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["email"] == "johndoe@example.com"

def test_find_all_users(setup_db):
    # Create a user first
    client.post(
        "/api/v1/user/",
        json={
            "name": "Jane Doe",
            "email": "janedoe@example.com",
            "mobile_number": 9876543210,
            "location": "Another Location",
            "password": "Password123!"
        }
    )
    
    response = client.get("/api/v1/user/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)  # Expect a list of users

def test_get_user(setup_db):
    # Create a user first
    create_response = client.post(
        "/api/v1/user/",
        json={
            "name": "Alice Smith",
            "email": "alicesmith@example.com",
            "mobile_number": 1122334455,
            "location": "Some Location",
            "password": "Password123!"
        }
    )
    user_id = create_response.json()["id"]

    # Test getting the user
    response = client.get(f"/api/v1/user/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "alicesmith@example.com"

def test_update_user(setup_db):
    # Create a user first
    create_response = client.post(
        "/api/v1/user/",
        json={
            "name": "Bob Brown",
            "email": "bobbrown@example.com",
            "mobile_number": 2233445566,
            "location": "New Location",
            "password": "Password123!"
        }
    )
    user_id = create_response.json()["id"]

    # Test updating the user
    update_response = client.put(
        f"/api/v1/user/{user_id}",
        json={
            "name": "Bob Updated",
            "password": "NewPassword123!"
        }
    )
    assert update_response.status_code == 200
    data = update_response.json()
    assert data["name"] == "Bob Updated"

def test_delete_user(setup_db):
    # Create a user first
    create_response = client.post(
        "/api/v1/user/",
        json={
            "name": "Charlie Black",
            "email": "charlieblack@example.com",
            "mobile_number": 6677889900,
            "location": "Delete Location",
            "password": "Password123!"
        }
    )
    user_id = create_response.json()["id"]

    # Test deleting the user
    delete_response = client.delete(f"/api/v1/user/{user_id}")
    assert delete_response.status_code == 200
    assert delete_response.json() == {"message": f"User with id {user_id} deleted successfully"}

    # Verify user is deleted
    get_response = client.get(f"/api/v1/user/{user_id}")
    assert get_response.status_code == 404
    assert get_response.json()["detail"] == f"User with id {user_id} not found"


def test_create_user_with_existing_email(setup_db):
    # Create a user first
    client.post("/api/v1/user/", json={
        "name": "ExistingUser",
        "email": "existing@example.com",
        "mobile_number": 1234567890,
        "location": "Chicago",
        "password": "Passw0rd!"
    })

    # Try creating another user with the same email
    response = client.post("/api/v1/user/", json={
        "name": "AnotherUser",
        "email": "existing@example.com",
        "mobile_number": 9876543210,
        "location": "San Francisco",
        "password": "Passw0rd!"
    })

    assert response.status_code == 422
    error_message = response.json().get("detail") or response.json().get("message")
    
    # Adjust assertion to handle the prefix
    expected_message = "User with this email already exists"
    assert expected_message in error_message, f"Expected '{expected_message}' but got '{error_message}'"

# def test_find_all_users_no_users(setup_db):
#     # Test when there are no users in the database
#     response = client.get("/api/v1/user/")
#     assert response.status_code == 404
#     assert response.json() == {"detail": "No users found"}

def test_create_user_invalid_data(setup_db):
    # Test missing required fields (email, password, mobile_number, and location)
    response = client.post(
        "/api/v1/user/",
        json={
            "name": "Invalid User",  # Name is provided
            "email": None,  # Missing email
            "password": None,  # Missing password
            "mobile_number": None,  # Missing mobile number
            "location": None  # Missing location
        }
    )
    assert response.status_code == 422  # Validation error
    

def test_update_user_no_changes(setup_db):
    # Create a user first
    create_response = client.post(
        "/api/v1/user/",
        json={
            "name": "Bob Brown",
            "email": "bobb@example.com",
            "mobile_number": 2233445566,
            "location": "New Location",
            "password": "Password123!"
        }
    )
    
    assert create_response.status_code == 201, f"User creation failed: {create_response.json()}"
    
    create_data = create_response.json()
    assert "id" in create_data, f"Expected 'id' in response, got {create_data}"
    
    user_id = create_data["id"]

    # Attempt to update the user with the same data
    update_response = client.put(
        f"/api/v1/user/{user_id}",
        json={
            "name": "Bob Brown",  # No actual changes
            "password": "Password123!"
        }
    )
    assert update_response.status_code == 400, f"Unexpected response: {update_response.json()}"
    assert update_response.json()["detail"] == "Failed to update user"


def test_get_user_not_found(setup_db):
    # Attempt to get a non-existent user
    response = client.get("/api/v1/user/9999")  # Non-existent user ID
    assert response.status_code == 404
    assert response.json() == {"detail": "User with id 9999 not found"}

def test_delete_user_not_found(setup_db):
    # Attempt to delete a non-existent user
    response = client.delete("/api/v1/user/9999")  # Non-existent user ID
    assert response.status_code == 404
    assert response.json() == {"detail": "User with id 9999 not found"}
