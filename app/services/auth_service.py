# Authentication Service
# This module will contain authentication-related business logic

from app.services.jwt_service import create_jwt, decode_jwt
from app.services.email_service import EmailService
from app.orm.engine import SessionLocal
from app.models.user import DatabaseUser
from email_validator import validate_email, EmailNotValidError
from fastapi import HTTPException, status
from app.orm.db_user import User
from hashlib import sha256
import random
import time
from datetime import datetime, timedelta
from typing import Dict


class AuthService:
    """
    Service class for handling authentication operations
    """
    
    # In-memory storage for password reset codes
    _reset_codes: Dict[str, Dict] = {}
    
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
    async def request_password_reset(email: str):
        """
        Generate and send password reset code
        """
        try:
            email = validate_email(email).email
        except EmailNotValidError:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Invalid email address"
            )
        
        session = SessionLocal()
        try:
            # Check if user exists (but don't reveal if they don't for security)
            user = session.query(User).filter_by(email=email).first()
            
            # Generate 6-digit code
            code = f"{random.randint(100000, 999999)}"
            
            # Store code with expiry (15 minutes)
            expiry_time = datetime.now() + timedelta(minutes=15)
            AuthService._reset_codes[email] = {
                "code": code,
                "expires_at": expiry_time,
                "user_exists": user is not None
            }
            
            # Only send email if user exists
            if user:
                await EmailService.send_reset_code(email, code)
            
            session.close()
            return True
            
        except Exception as e:
            session.rollback()
            print(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error processing password reset request"
            )
    
    @staticmethod
    async def reset_password_with_code(email: str, code: str, new_password: str):
        """
        Reset password using verification code
        """
        try:
            email = validate_email(email).email
        except EmailNotValidError:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Invalid email address"
            )
        
        if len(new_password) < 8:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Password must be at least 8 characters long"
            )
        
        # Check if reset code exists and is valid
        reset_data = AuthService._reset_codes.get(email)
        if not reset_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired reset code"
            )
        
        # Check if code matches
        if reset_data["code"] != code:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid reset code"
            )
        
        # Check if code is expired
        if datetime.now() > reset_data["expires_at"]:
            # Clean up expired code
            del AuthService._reset_codes[email]
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Reset code has expired"
            )
        
        # Check if user actually exists
        if not reset_data["user_exists"]:
            # Clean up code
            del AuthService._reset_codes[email]
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid reset code"
            )
        
        session = SessionLocal()
        try:
            # Get user and update password
            user = session.query(User).filter_by(email=email).first()
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid reset code"
                )
            
            # Update password with same hashing method as registration
            hashed_password = sha256(new_password.encode('utf-8')).hexdigest()
            user.password = hashed_password
            
            session.commit()
            
            # Clean up used reset code
            del AuthService._reset_codes[email]
            
            session.close()
            return True
            
        except Exception as e:
            session.rollback()
            print(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error updating password"
            )

    
    @staticmethod
    async def authenticate_user(email: str, password: str):
        """
        Authenticate user credentials
        """
        try:
            email = validate_email(email).email
        except EmailNotValidError:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Invalid email address"
            )
        
        session = SessionLocal()
        try:
            # Get user from database
            user = session.query(User).filter_by(email=email).first()
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid email or password"
                )
            
            # Hash the provided password and compare with stored hash
            hashed_password = sha256(password.encode('utf-8')).hexdigest()
            
            if user.password != hashed_password:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid email or password"
                )
            
            session.close()
            return user
            
        except HTTPException:
            session.close()
            raise
        except Exception as e:
            session.rollback()
            print(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error during authentication"
            )
    
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
