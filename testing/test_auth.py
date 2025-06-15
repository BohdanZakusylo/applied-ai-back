from fastapi.testclient import TestClient
from app.main import app
import random

client = TestClient(app)

def generate_random_email():
    words = ["apple", "blue", "cloud", "delta", "echo", "fox", "green", "honey", "iris", "jazz", "kite", "lava", "mint", "nova", "opal", "pink", "quiz", "rose", "star", "tree"]
    random_words = "-".join(random.sample(words, 4))
    return f"{random_words}@gmail.com"

def test_register_user_status_only():
    email = generate_random_email()
    user_data = {
        "email": email,
        "password": "testpassword123",
        "name": "Test User",
        "insurance_provider": "Test Insurance",
        "general_practitioner": "Dr. Test",
        "medical_information": "No known allergies"
    }

    response = client.post("/api/v1/auth/register", json=user_data)
    assert response.status_code == 201