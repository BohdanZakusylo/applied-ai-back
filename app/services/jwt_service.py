import datetime
import jwt
import os
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

PRIVATE_KEY_PATH = "app/keys/private_key.pem"
PUBLIC_KEY_PATH = "app/keys/public_key.pem"

def ensure_keys_exist():
    """Generate RSA keys if they don't exist"""
    if not os.path.exists(PRIVATE_KEY_PATH) or not os.path.exists(PUBLIC_KEY_PATH):
        print("🔑 Generating RSA keys for JWT...")
        os.makedirs("app/keys", exist_ok=True)
        
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        with open(PRIVATE_KEY_PATH, "wb") as f:
            f.write(private_key.private_bytes(
                serialization.Encoding.PEM,
                serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            ))

        public_key = private_key.public_key()
        with open(PUBLIC_KEY_PATH, "wb") as f:
            f.write(public_key.public_bytes(
                serialization.Encoding.PEM,
                serialization.PublicFormat.SubjectPublicKeyInfo
            ))
        print("✅ RSA key pair generated at app/keys/")

def load_keys():
    ensure_keys_exist()  # Generate keys if they don't exist
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
    _, public_key = load_keys()
    payload = jwt.decode(token, public_key, algorithms=["RS256"])

    issue_time = datetime.datetime.fromisoformat(payload["issue_time"])
    lifetime = datetime.timedelta(minutes=payload["lifetime_minutes"])
    now = datetime.datetime.utcnow()

    if now > issue_time + lifetime:
        raise Exception("Token expired")

    return payload
