import jwt
import datetime

PRIVATE_KEY_PATH = "app/keys/private_key.pem"
PUBLIC_KEY_PATH = "app/keys/public_key.pem"

def load_keys():
    with open(PRIVATE_KEY_PATH, "rb") as f:
        private_key = f.read()
    with open(PUBLIC_KEY_PATH, "rb") as f:
        public_key = f.read()
    return private_key, public_key

def create_jwt(user_id: int) -> str:
    private_key, _ = load_keys()
    payload = {
        "user_id": user_id,
        "issue_time": datetime.datetime.utcnow().isoformat(),
        "expiration_time": (datetime.datetime.utcnow() + datetime.timedelta(hours=1)).isoformat()
    }
    return jwt.encode(payload, private_key, algorithm="RS256")

def decode_jwt(token: str) -> dict:
    _, public_key = load_keys()
    return jwt.decode(token, public_key, algorithms=["RS256"])
