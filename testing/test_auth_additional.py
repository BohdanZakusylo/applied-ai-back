from fastapi.testclient import TestClient
from app.main import app
from testing.test_auth import generate_random_email

client = TestClient(app)

def test_login_success():
    # First register a user
    email = generate_random_email()
    password = "testpassword123"
    user_data = {
        "email": email,
        "password": password,
        "name": "Test User",
        "insurance_provider": "Test Insurance",
        "general_practitioner": "Dr. Test",
        "medical_information": "No known allergies"
    }
    
    register_response = client.post("/api/v1/auth/register", json=user_data)
    assert register_response.status_code == 201
    
    login_data = {
        "email": email,
        "password": password
    }
    response = client.post("/api/v1/auth/login", json=login_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "token_type" in data
    assert data["token_type"] == "bearer"

def test_login_invalid_credentials():
    login_data = {
        "email": "nonexistent@example.com",
        "password": "wrongpassword"
    }
    response = client.post("/api/v1/auth/login", json=login_data)
    assert response.status_code == 422

def test_login_incorrect_credentials():
    login_data = {
        "email": "qq@gmail.com",
        "password": "wrongpassword"
    }
    response = client.post("/api/v1/auth/login", json=login_data)
    assert response.status_code == 401

def test_logout():
    # First register and login to get a token
    email = generate_random_email()
    user_data = {
        "email": email,
        "password": "testpassword123",
        "name": "Test User"
    }
    
    register_response = client.post("/api/v1/auth/register", json=user_data)
    assert register_response.status_code == 201
    
    login_response = client.post("/api/v1/auth/login", json={
        "email": email,
        "password": "testpassword123"
    })
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    
    # Test logout
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/api/v1/auth/logout", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "logged out successfully" in data["message"]

def test_forgot_password():
    # First register a user
    email = generate_random_email()
    user_data = {
        "email": email,
        "password": "testpassword123",
        "name": "Test User"
    }
    
    register_response = client.post("/api/v1/auth/register", json=user_data)
    assert register_response.status_code == 201
    
    # Test forgot password
    forgot_password_data = {
        "email": email
    }
    response = client.post("/api/v1/auth/forgot-password", json=forgot_password_data)
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "sent to your email" in data["message"]