import datetime
import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
import os
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

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
    issue_time = datetime.datetime.utcnow()
    lifetime = datetime.timedelta(hours=1)

    payload = {
        "user_id": user_id,
        "issue_time": issue_time.isoformat(),
        "lifetime_minutes": lifetime.total_seconds() / 60
    }

    return jwt.encode(payload, private_key, algorithm="RS256")

def decode_jwt(token: str) -> dict:
    try:
        _, public_key = load_keys()
        payload = jwt.decode(token, public_key, algorithms=["RS256"])

        # Validate custom expiration manually
        issue_time = datetime.datetime.fromisoformat(payload["issue_time"])
        lifetime = datetime.timedelta(minutes=payload["lifetime_minutes"])
        now = datetime.datetime.utcnow()

        if now > issue_time + lifetime:
            raise Exception("Token expired (manual check)")

        return payload

    except ExpiredSignatureError:
        raise Exception("Token has expired")

    except InvalidTokenError:
        raise Exception("Invalid token")

    except KeyError as e:
        raise Exception(f"Missing claim in token")

    except Exception as e:
        raise Exception(f"Failed to decode token")
