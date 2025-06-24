from ..base import Base
from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

class Message(Base):
    __tablename__ = "message"

    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, ForeignKey("chat.id", ondelete="CASCADE"), nullable=False)

    chat = relationship("Chat", back_populates="messages")
    message = Column(Text, nullable=False)
    isIncoming = Column(Boolean, nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)

