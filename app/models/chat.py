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
    id: int
    message: str
    isIncoming: bool
    created_at: datetime


class ChatHistoryResponse(BaseModel):
    conversations: List[ConversationHistory]
    message: str

class NewCratedChatResponse(BaseModel):
    response: str
    chat_name: str

class GetHistory(BaseModel):
    chat_name: str

class GetChats(BaseModel):
    chat_names: List[str]

class DeleteChat(BaseModel):
    response: str