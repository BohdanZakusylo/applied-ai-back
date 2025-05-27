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
    first_name: Optional[str] = None
    last_name: Optional[str] = None

class UserProfileResponse(BaseModel):
    user: DatabaseUser
    message: str 