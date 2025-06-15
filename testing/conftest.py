import pytest
from fastapi.testclient import TestClient
from app.main import app
from test_auth import generate_random_email

client = TestClient(app)

@pytest.fixture
def test_user_token():
    email = generate_random_email()
    password = "testpassword123"

    user_data = {
        "email": email,
        "password": password,
        "name": "Test User",
        "insurance_provider": "Test Insurance",
        "general_practitioner": "Dr. Test",
        "medical_information": "None"
    }

    register_response = client.post("/api/v1/auth/register", json=user_data)
    assert register_response.status_code == 201

    login_response = client.post("/api/v1/auth/login", json={
        "email": email,
        "password": password
    })
    assert login_response.status_code == 200

    token = login_response.json()["access_token"]
    return token