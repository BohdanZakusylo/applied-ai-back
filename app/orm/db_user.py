from .base import Base

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from typing import Optional

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    email: Mapped[str] = mapped_column(String(30))
    password: Mapped[str] = mapped_column(String(256))
    insurance_provider: Mapped[Optional[str]] = mapped_column(String(30))
    general_practitioner: Mapped[Optional[str]] = mapped_column(String(30))
    medical_information: Mapped[Optional[str]] = mapped_column(String(30))
