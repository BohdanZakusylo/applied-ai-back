# User Service
# This module will contain user-related business logic

from app.orm.engine import SessionLocal
from app.orm.db_user import User
from fastapi import HTTPException, status
from email_validator import validate_email, EmailNotValidError
from hashlib import sha256
from datetime import datetime

# Configuration
MONTHLY_QUESTION_LIMIT = 100

class UserService:
    """
    Service class for handling user operations
    """
    
    @staticmethod
    def get_user_by_id(user_id: int):
        """
        Get user profile by ID
        """
        db = SessionLocal()
        try:
          user = db.query(User).filter(User.id == user_id).first()
          if not user:
            raise HTTPException(
              status_code=404,
              detail="User not found"
              )
          return user
        except HTTPException: 
            # Re-raise HTTPExceptions so they reach the client with correct status codes
            db.close()
            raise
        except Exception as e:
            db.rollback()
            print(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal error getting user."
            )
        finally:
          db.close()
    
    @staticmethod
    async def update_user_profile(user_id: str, email=None, password=None, insurance_provider=None, general_practitioner=None, medical_information=None):
        """
        Update user profile
        """
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                raise HTTPException(
                  status_code=404,
                  detail="User not found"
                  )

            if email is not None:
                try:
                    email = validate_email(email).email
                except EmailNotValidError:
                    raise HTTPException(
                        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                        detail="Invalid email address"
                    )

                existing = db.query(User).filter_by(email=email).first()
                if existing and existing.id != user.id:
                    raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail="User with this email already exists."
                    )
                user.email = email

            if password is not None:
                if len(password) < 8:
                    raise HTTPException(
                        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                        detail="Password must be at least 8 characters long."
                    )

                hashed_password_sha256 = sha256(password.encode('utf-8')).hexdigest()
                user.password = hashed_password_sha256

            if insurance_provider is not None:
                user.insurance_provider = insurance_provider

            if general_practitioner is not None:
                user.general_practitioner = general_practitioner

            if medical_information is not None:
                user.medical_information = medical_information

            db.commit()
            db.refresh(user)

            return user

        except HTTPException:
            db.close()
            raise

        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal error updating user."
            )

        finally:
            db.close()
    
    @staticmethod
    async def delete_user_account(user_id: str):
        """
        Delete user account and all associated data
        TODO: Implement account deletion logic
        """
        pass
    
    @staticmethod
    async def check_user_exists(email: str):
        """
        Check if user exists by email
        TODO: Implement user existence check
        """
        pass
    
    @staticmethod
    def check_and_increment_monthly_questions(user_id: int):
        """
        Check if user has remaining questions for the month and increment count if allowed
        Returns True if question is allowed, False if limit exceeded
        """
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                raise HTTPException(
                    status_code=404,
                    detail="User not found"
                )
            
            current_month_year = datetime.now().strftime("%Y-%m")
            
            # Reset count if it's a new month
            if user.current_month_year != current_month_year:
                user.monthly_questions_used = 0
                user.current_month_year = current_month_year
            
            # Check if user has exceeded the monthly limit
            if user.monthly_questions_used >= MONTHLY_QUESTION_LIMIT:
                return False
            
            # Increment the count
            user.monthly_questions_used += 1
            db.commit()
            
            return True
            
        except HTTPException:
            db.close()
            raise
        except Exception as e:
            db.rollback()
            print(f"Error checking monthly questions: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal error checking question limit."
            )
        finally:
            db.close()
    
    @staticmethod
    def get_monthly_questions_remaining(user_id: int):
        """
        Get the number of questions remaining for the month
        """
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                raise HTTPException(
                    status_code=404,
                    detail="User not found"
                )
            
            current_month_year = datetime.now().strftime("%Y-%m")
            
            # Reset count if it's a new month
            if user.current_month_year != current_month_year:
                return MONTHLY_QUESTION_LIMIT
            
            return max(0, MONTHLY_QUESTION_LIMIT - user.monthly_questions_used)
            
        except HTTPException:
            db.close()
            raise
        except Exception as e:
            db.rollback()
            print(f"Error getting monthly questions remaining: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal error getting question limit."
            )
        finally:
            db.close() 