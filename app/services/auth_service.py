# Authentication Service
# This module will contain authentication-related business logic

from app.services.jwt_service import create_jwt, decode_jwt
from app.orm.engine import SessionLocal
from app.models.user import DatabaseUser
from email_validator import validate_email, EmailNotValidError
from fastapi import HTTPException, status
from app.orm.db_user import User
from hashlib import sha256


class AuthService:
    """
    Service class for handling authentication operations
    """
    
    @staticmethod
    async def register_user(email, password, name, insurance_provider : str | None = None, general_practitioner : str | None = None, medical_information : str | None = None):
        if(not email or not password or not name):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Some fields are missing"
            )
        try:
            email = validate_email(email).email
        except EmailNotValidError as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Invalid email address"
            )
        
        if len(password) < 8:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Password must be at least 8 characters long."
            )
        
        session = SessionLocal()
        try:
            existing = session.query(User).filter_by(email=email).first()
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="A user with that email already exists."
                )
            hashed_password_sha256 = sha256(password.encode('utf-8')).hexdigest();

            user = User(
                email=email,
                password=hashed_password_sha256,
                name=name,
                insurance_provider=insurance_provider,
                general_practitioner=general_practitioner,
                medical_information=medical_information
            )

            session.add(user)
            session.commit()
            session.refresh(user)

            return user
    

        except Exception as e:
            session.rollback();
            print(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal error registering user."
            ) 



    
    @staticmethod
    async def authenticate_user(email: str, password: str):
        """
        Authenticate user credentials
        TODO: Implement user authentication logic
        """
        pass
    
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
