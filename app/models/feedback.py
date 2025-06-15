from pydantic import BaseModel, EmailStr, constr
from typing import Optional, Literal

class FeedbackCreate(BaseModel):
    category: Literal[
        "General Feedback",
        "Bug Report",
        "Feature Suggestion",
        "Something didn’t work as expected"
    ]
    message: constr(min_length=1, max_length=1000)
    email: Optional[EmailStr] = None
