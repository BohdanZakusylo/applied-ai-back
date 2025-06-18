import datetime
import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
import os
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from app.orm.engine import SessionLocal
from app.orm.db_user import User

PRIVATE_KEY_PATH = "/etc/secrets/private_key.pem"
PUBLIC_KEY_PATH = "/etc/secrets/public_key.pem"

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
    expiry_time = issue_time + lifetime

    payload = {
        "user_id": user_id,
        "issue_time": issue_time.isoformat(),
        "lifetime_minutes": lifetime.total_seconds() / 60,
        "expires_at": expiry_time.isoformat()
    }

    token = jwt.encode(payload, private_key, algorithm="RS256")
    
    # Store token in user record
    session = SessionLocal()
    try:
        # Update user record with new token
        user = session.query(User).filter(User.id == user_id).first()
        if user:
            user.token = token
            session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

    return token

def decode_jwt(token: str) -> dict:
    try:
        # Verify token signature first
        _, public_key = load_keys()
        payload = jwt.decode(token, public_key, algorithms=["RS256"])
        
        # Get user and verify token matches the one stored
        user_id = payload["user_id"]
        session = SessionLocal()
        user = session.query(User).filter(User.id == user_id).first()
        
        if not user or user.token != token:
            session.close()
            raise Exception("Invalid token or token has been revoked")
        
        # Validate expiration
        now = datetime.datetime.utcnow()
        issue_time = datetime.datetime.fromisoformat(payload["issue_time"])
        lifetime = datetime.timedelta(minutes=payload["lifetime_minutes"])
        
        if now > issue_time + lifetime:
            # Token is expired - could clear it from the user record
            # but we'll leave that for the logout functionality
            session.close()
            raise Exception("Token expired")
            
        session.close()
        return payload

    except ExpiredSignatureError:
        raise Exception("Token has expired")

    except InvalidTokenError:
        raise Exception("Invalid token")

    except KeyError as e:
        raise Exception(f"Missing claim in token")

    except Exception as e:
        raise Exception(f"Failed to decode token: {str(e)}")

def invalidate_token(token: str) -> bool:
    """Invalidate a specific token by setting the user's token to None"""
    try:
        # Verify token signature first to get the user_id
        _, public_key = load_keys()
        payload = jwt.decode(token, public_key, algorithms=["RS256"])
        
        user_id = payload.get("user_id")
        if not user_id:
            return False
            
        # Find the user and clear their token
        session = SessionLocal()
        try:
            user = session.query(User).filter(User.id == user_id).first()
            
            # Only clear if this is the current token
            if user and user.token == token:
                user.token = None
                session.commit()
                session.close()
                return True
            else:
                session.close()
                return False
        except Exception as e:
            session.rollback()
            session.close()
            return False
    except Exception:
        # If token can't be decoded, just return False
        return False
