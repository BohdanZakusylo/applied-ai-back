from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_feedback_success(test_user_token):
    headers = {"Authorization": f"Bearer {test_user_token}"}
    feedback_data = {
        "category": "General Feedback",
        "message": "<script>alert('XSS')</script>This is feedback.",
        "email": "user@example.com"
    }

    response = client.post("/api/v1/feedback", json=feedback_data, headers=headers)

    assert response.status_code == 201
    data = response.json()
    assert data["message"] == "Feedback submitted successfully."

def test_create_feedback_unauthorized():
    feedback_data = {
        "category": "General",
        "message": "Unauthorized attempt",
        "email": "noauth@example.com"
    }

    response = client.post("/api/v1/feedback", json=feedback_data)

    assert response.status_code == 403
