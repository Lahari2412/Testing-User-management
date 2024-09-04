import pytest
from fastapi.testclient import TestClient
from main import app  # Ensure you import the FastAPI app correctly
from config.db import conn

client = TestClient(app)

@pytest.fixture
def setup_db():
    user_collection = conn.local.user
    user_collection.delete_many({})  # Clear the user collection
    # Insert a test user
    user_collection.insert_one({
        "email": "test@example.com",
        "password": "OldHashedPassword123!"  # Assuming a pre-hashed password
    })
    yield
    # Teardown: Clear the database after each test
    user_collection.delete_many({})

def test_reset_password_success(setup_db):
    # Test case for successful password reset
    response = client.put(
        "/api/v1/password_reset/test@example.com",
        json={"new_password": "NewPassword123!"}
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Password reset successful"}

    # Verify password has been updated in the database
    user_collection = conn.local.user
    updated_user = user_collection.find_one({"email": "test@example.com"})
    assert updated_user is not None
    assert updated_user["password"] != "OldHashedPassword123!"  # Password should be changed

def test_reset_password_user_not_found(setup_db):
    # Test case for a non-existent user
    response = client.put(
        "/api/v1/password_reset/nonexistent@example.com",
        json={"new_password": "NewPassword123!"}
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "User with the given email not found"}

def test_reset_password_invalid_password(setup_db):
    # Test case for password that doesn't meet validation criteria
    response = client.put(
        "/api/v1/password_reset/test@example.com",
        json={"new_password": "short"}
    )
    assert response.status_code == 422
    assert response.json() == {"message": "Password must be at least 8 characters long"}