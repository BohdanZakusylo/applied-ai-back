from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class DatabaseUser(BaseModel):
    id: int
    name: str
    email: str
    password: str
    insurance_provider: str
    general_practitioner: str
    medical_information: str

class UserProfileUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    token: Optional[str] = None
    insurance_provider: Optional[str] = None
    general_practitioner: Optional[str] = None
    medical_information: Optional[str] = None

class UserProfileResponse(BaseModel):
    user: DatabaseUser
    message: str 