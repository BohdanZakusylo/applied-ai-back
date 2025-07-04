from pydantic import BaseModel, EmailStr
from typing import Optional

class UserRegister(BaseModel):
    email: EmailStr
    password: str
    name: str
    insurance_provider: Optional[str] = None
    general_practitioner: Optional[str] = None
    medical_information: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    expires_in: int

class ForgotPassword(BaseModel):
    email: EmailStr

class ResetPassword(BaseModel):
    email: EmailStr
    code: str
    new_password: str

class AuthResponse(BaseModel):
    message: str
    #we dont have it as of now
    # user_id: Optional[str] = None 