from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class DeadlineBase(BaseModel):
    title: str
    due_date: datetime


class DeadlineCreate(DeadlineBase):
    pass


class DeadlineUpdate(BaseModel):
    title: Optional[str] = None
    due_date: Optional[datetime] = None


class DeadlineResponse(DeadlineBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class DeadlineListResponse(BaseModel):
    items: List[DeadlineResponse]
    total: int
