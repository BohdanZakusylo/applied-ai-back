from fastapi.testclient import TestClient
from app.main import app
from testing.test_auth import generate_random_email

client = TestClient(app)


def test_get_user_profile(test_user_token):
    headers = {"Authorization": f"Bearer {test_user_token}"}
    
    response = client.get("/api/v1/users/profile", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "user" in data

def test_update_user_profile(test_user_token):
    headers = {"Authorization": f"Bearer {test_user_token}"}
    update_data = {
        "email": generate_random_email(),
        "insurance_provider": "Updated Insurance",
        "general_practitioner": "Dr. Updated",
        "medical_information": "Updated medical info"
    }
    
    response = client.put("/api/v1/users/profile", json=update_data, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "updated_user" in data
    assert data["updated_user"]["insurance_provider"] == "Updated Insurance"

def test_delete_user_account(test_user_token):
    headers = {"Authorization": f"Bearer {test_user_token}"}
    
    response = client.delete("/api/v1/users/profile", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "deleted successfully" in data["message"] 