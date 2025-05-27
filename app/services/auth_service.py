# Authentication Service
# This module will contain authentication-related business logic

from app.services.jwt_service import create_jwt, decode_jwt

from hashlib import sha256
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.orm.db_user import User
from app.orm.engine import SessionLocal
from app.services.jwt_service import create_jwt

class AuthService:
    """
    Service class for handling authentication operations
    """
    
    @staticmethod
    async def register_user(email: str, password: str, first_name: str = None, last_name: str = None):
        """
        Register a new user
        TODO: Implement user registration logic
        """
        pass
    
    @staticmethod
    async def authenticate_user(email: str, password: str):
        session = SessionLocal()
        try:
            stmt = select(User).where(User.email == email)
            user = session.scalars(stmt).first()

            if not user:
                return None

            hashed_input_pw = sha256(password.strip().encode('utf-8')).hexdigest()

            if user.password != hashed_input_pw:
                return None

            return user
        finally:
            session.close()

    @staticmethod
    async def create_access_token(user_id: str):
        return create_jwt(user_id)
    
    @staticmethod
    async def create_access_token(user_id: str):
        return create_jwt(user_id)
    
    @staticmethod
    async def verify_token(token: str):
        try:
          return decode_jwt(token)
        except Exception as e:
          return {"error": str(e)}
    
    @staticmethod
    async def send_password_reset_email(email: str):
        """
        Send password reset email
        TODO: Implement password reset email functionality
        """
        pass 