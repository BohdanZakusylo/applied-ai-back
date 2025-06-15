from .base import Base
from sqlalchemy import Column, Integer, String, Text

class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    email = Column(String, nullable=True)
