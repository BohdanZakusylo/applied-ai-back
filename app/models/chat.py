from pydantic import BaseModel
from typing import List
from datetime import datetime

class ChatMessage(BaseModel):
    message: str
    chat_name: str

class ChatResponse(BaseModel):
    response: str
    message_id: str
    timestamp: datetime

# remove if unused
class ConversationHistory(BaseModel):
    id: str
    user_message: str
    ai_response: str
    timestamp: datetime

class ChatHistoryResponse(BaseModel):
    conversations: List[ConversationHistory]
    total_count: int

class NewCratedChatResponse(BaseModel):
    response: str