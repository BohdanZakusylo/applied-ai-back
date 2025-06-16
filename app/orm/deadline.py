from .base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, DateTime
from typing import Optional
from datetime import datetime


class Deadline(Base):
    __tablename__ = "deadlines"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    due_date: Mapped[datetime] = mapped_column(DateTime)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    # We could add more fields like:
    # description: Mapped[Optional[str]] = mapped_column(String(500))
    # status: Mapped[str] = mapped_column(String(20))  # e.g., "pending", "completed", "overdue"
    # priority: Mapped[Optional[str]] = mapped_column(String(20))  # e.g., "high", "medium", "low"
