import pytest
from fastapi.testclient import TestClient
from main import app, get_password_hash
from config.db import conn
from bson.objectid import ObjectId
import bcrypt

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    conn.local.user.delete_many({})
    yield
    conn.local.user.delete_many({})


def test_find_admin(setup_db):
    # Create a user first
    client.post(
        "/api/v1/user/",
        json={
            "name": "Admin",
            "email": "admin@gmail.com",
            "mobile_number": 9876543210,
            "location": "Another Location",
            "password": "Admin@12345"
        }
    )
    
    response = client.get("/api/v1/user/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)  # Expect a list of users


def test_create_user():
    user_data = {
        "name": "Admin",
        "email": "admin@gmail.com",
        "mobile_number": 9876543210,
        "location": "Test City",
        "password": "Admin@12345",
        "role": "user",
        "whatsapp_api_token": None,
        "whatsapp_cloud_number_id": None
    }
    response = client.post("/api/v1/user", json=user_data)  # Replace with the actual endpoint for user creation
    assert response.status_code == 201
    created_user = conn.local.user.find_one({"email": "admin@gmail.com"})
    assert created_user is not None
    assert created_user["name"] == "Admin"
 
 
def test_password_hashing():
    raw_password = "Admin@12345"
    hashed_password = get_password_hash(raw_password)
    assert hashed_password != raw_password
    assert bcrypt.checkpw(raw_password.encode('utf-8'), hashed_password.encode('utf-8'))

