import datetime
import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
import os
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from app.orm.engine import SessionLocal
from app.orm.db_token import Token

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
    expiry_time = issue_time + lifetime

    payload = {
        "user_id": user_id,
        "issue_time": issue_time.isoformat(),
        "lifetime_minutes": lifetime.total_seconds() / 60
    }

    token = jwt.encode(payload, private_key, algorithm="RS256")
    
    # Store token in database
    session = SessionLocal()
    try:
        # Invalidate previous tokens for this user
        session.query(Token).filter(
            Token.user_id == user_id,
            Token.is_active == True
        ).update({"is_active": False})
        
        # Create new token record
        db_token = Token(
            user_id=user_id,
            token=token,
            is_active=True,
            expires_at=expiry_time
        )
        session.add(db_token)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

    return token

def decode_jwt(token: str) -> dict:
    try:
        # First check if token is in database and active
        session = SessionLocal()
        db_token = session.query(Token).filter(
            Token.token == token,
            Token.is_active == True
        ).first()
        
        if not db_token:
            session.close()
            raise Exception("Token not found or inactive")
        
        # Check if token has expired in database
        now = datetime.datetime.utcnow()
        if now > db_token.expires_at:
            # Mark token as inactive
            db_token.is_active = False
            session.commit()
            session.close()
            raise Exception("Token expired")
        
        # Verify token signature
        _, public_key = load_keys()
        payload = jwt.decode(token, public_key, algorithms=["RS256"])

        # Validate custom expiration manually
        issue_time = datetime.datetime.fromisoformat(payload["issue_time"])
        lifetime = datetime.timedelta(minutes=payload["lifetime_minutes"])
        if now > issue_time + lifetime:
            # Mark token as inactive
            db_token.is_active = False
            session.commit()
            session.close()
            raise Exception("Token expired (manual check)")
            
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
    """Invalidate a specific token"""
    session = SessionLocal()
    try:
        db_token = session.query(Token).filter(
            Token.token == token,
            Token.is_active == True
        ).first()
        
        if db_token:
            db_token.is_active = False
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
