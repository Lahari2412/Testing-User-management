import pytest
from fastapi.testclient import TestClient
from main import app
from config.db import conn
from bcrypt import hashpw, gensalt

client = TestClient(app)

@pytest.fixture(scope="module")
def setup_db():
    conn.local.user.drop()
    yield
    conn.local.user.drop()

def create_user(email: str, password: str):
    hashed_password = hashpw(password.encode('utf-8'), gensalt()).decode('utf-8')
    conn.local.user.insert_one({
        "email": email,
        "password": hashed_password,
        "role": "user",
        "id": 1
    })

def test_login_successful(setup_db):
    create_user("testuser@example.com", "ValidPassword123!")
    
    response = client.post(
        "/api/v1/login/",
        json={
            "email": "testuser@example.com",
            "password": "ValidPassword123!"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Login Successful"


def test_login_invalid_password(setup_db):
    create_user("testuser@example.com", "ValidPassword123!")
    
    response = client.post(
        "/api/v1/login/",
        json={
            "email": "testuser@example.com",
            "password": "InValidPassword13!2"
        }
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid email or password"}

def test_login_non_existent_user(setup_db):
    response = client.post(
        "/api/v1/login/",
        json={
            "email": "nonexistentuser@example.com",
            "password": "SomePassword123!"
        }
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}
