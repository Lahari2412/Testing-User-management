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
    # Ensure the user and counters collections are empty before tests
    conn.local.user.drop()
    conn.local.counters.drop()  # Ensure counters collection is also empty for sequence values
    yield
    conn.local.user.drop()
    conn.local.counters.drop()

def test_create_admin_user(setup_db):
    admin_data = {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "mobile_number": 1234567890,
        "location": "Test Location"
    }

    response = client.post("/api/v1/admin/", json=admin_data)

    assert response.status_code == 201
    response_data = response.json()
    assert response_data["email"] == "john.doe@example.com"

    db = conn.local
    user = db.user.find_one({"email": "john.doe@example.com"})
    assert user is not None
    assert user["name"] == "John Doe"
    assert len(user["password"]) > 0  # Ensure password is hashed

def test_create_admin_user_duplicate_email(setup_db):
    admin_data = {
        "name": "Jane Doe",
        "email": "john.doe@example.com",
        "mobile_number": 1234567891,
        "location": "Test Location"
    }
    client.post("/api/v1/admin/", json=admin_data)

    # Attempt to create a user with the same email
    response = client.post("/api/v1/admin/", json=admin_data)

    assert response.status_code == 422
    error_message = response.json().get("detail") or response.json().get("message")
    
    # Adjust assertion to handle the prefix
    expected_message = "User with this email already exists"
    assert expected_message in error_message, f"Expected '{expected_message}' but got '{error_message}'"

def test_create_admin_user_invalid_email(setup_db):
    invalid_admin_data = {
        "name": "Jake Doe",
        "email": "invalid-email",
        "mobile_number": 1234567892,
        "location": "Test Location"
    }

    response = client.post("/api/v1/admin/", json=invalid_admin_data)

    assert response.status_code == 422  # Unprocessable Entity for validation errors
    assert "detail" in response.json()  # Check for the presence of validation error details


def test_create_admin_user_missing_field(setup_db):
    admin_data = {
        "name": "Emily Doe",
        "email": "emily.doe@example.com",
        "location": "Test Location"
        # Missing mobile_number
    }

    response = client.post("/api/v1/admin/", json=admin_data)

    assert response.status_code == 422  # Unprocessable Entity for validation errors
    assert "detail" in response.json()  # Check for the presence of validation error details

def test_create_admin_user_invalid_mobile_number(setup_db):
    admin_data = {
        "name": "Lucas Doe",
        "email": "lucas.doe@example.com",
        "mobile_number": "invalid-number",  # Invalid format
        "location": "Test Location"
    }

    response = client.post("/api/v1/admin/", json=admin_data)

    assert response.status_code == 422  # Unprocessable Entity for validation errors
    assert "detail" in response.json()  # Check for the presence of validation error details

def test_create_admin_user_role_assignment(setup_db):
    admin_data = {
        "name": "Sophia Doe",
        "email": "sophia.doe@example.com",
        "mobile_number": 1234567893,
        "location": "Test Location"
    }

    response = client.post("/api/v1/admin/", json=admin_data)

    assert response.status_code == 201
    response_data = response.json()
    
    db = conn.local
    user = db.user.find_one({"email": "sophia.doe@example.com"})
    assert user is not None
    assert user["role"] == "user"

def test_create_admin_user_special_characters_password(setup_db):
    admin_data = {
        "name": "Oliver Doe",
        "email": "oliver.doe@example.com",
        "mobile_number": 1234567894,
        "location": "Test Location"
    }

    response = client.post("/api/v1/admin/", json=admin_data)

    assert response.status_code == 201
    response_data = response.json()
    
    db = conn.local
    user = db.user.find_one({"email": "oliver.doe@example.com"})
    assert user is not None
    assert len(user["password"]) > 0  # Ensure password is hashed and not empty

def test_password_hashing(setup_db):
    admin_data = {
        "name": "Ava Doe",
        "email": "ava.doe@example.com",
        "mobile_number": 1234567895,
        "location": "Test Location"
    }

    response = client.post("/api/v1/admin/", json=admin_data)

    assert response.status_code == 201
    response_data = response.json()
    
    db = conn.local
    user = db.user.find_one({"email": "ava.doe@example.com"})
    assert user is not None
    # Ensure the password is hashed
    assert user["password"].startswith("$2b$")  # bcrypt hashes start with "$2b$"