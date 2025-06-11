from .base import Base

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Boolean, ForeignKey, DateTime
from sqlalchemy.sql import func
from datetime import datetime

class Token(Base):
    __tablename__ = "tokens"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    token: Mapped[str] = mapped_column(String(500))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    expires_at: Mapped[datetime] = mapped_column(DateTime)
