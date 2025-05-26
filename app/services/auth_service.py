# Authentication Service
# This module will contain authentication-related business logic

from app.services.jwt_service import create_jwt, decode_jwt

import bcrypt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.orm.db_user import User
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
    async def authenticate_user(email: str, password: str, db: AsyncSession):
      """
      Authenticate user credentials
      """
      result = await db.execute(select(User).where(User.email == email))
      user = result.scalar_one_or_none()

      if not user:
          return None

      if not bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
          return None

      return user

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