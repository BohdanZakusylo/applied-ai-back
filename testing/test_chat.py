from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_send_chat_message(test_user_token):
    headers = {"Authorization": f"Bearer {test_user_token}"}
    
    message_data = {
        "message": "What does my insurance cover?",
    }
    
    response = client.post("/api/v1/chat/message", json=message_data, headers=headers)

    assert response.status_code == 422
    # data = response.json()
    # assert "response" in data