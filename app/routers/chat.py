import time
import os
import bleach

from openai import OpenAI
from fastapi import APIRouter, HTTPException, status, Depends
from app.models.chat import (
    ChatMessage, 
    ChatResponse, 
    ChatHistoryResponse, 
    ConversationHistory, 
)
from app.dependencies import get_current_user
from app.AI.integration.rag_service import RAGService
from datetime import datetime
from dotenv import load_dotenv
from app.services.chat_service import ChatService

router = APIRouter(prefix="/chat", tags=["Chat"])

chatService = ChatService()
# ITH-94: Integrate trained ChatpGPT with API
rag_service = RAGService()

load_dotenv();

@router.post("/message", response_model=ChatResponse)
async def send_message(user_message: ChatMessage, current_user: str = Depends(get_current_user)):
    if(current_user):
        API_KEY = os.getenv("GPT_API_KEY")
        ASS_ID = os.getenv("ASS_ID")

        ready_message = None
        try:
            client = OpenAI(api_key=API_KEY)

            empty_thread = client.beta.threads.create()
            sanitized_user_message = bleach.clean(
                user_message.message,
                tags=[],
                attributes={},
                strip=True
            )
            thread_message = client.beta.threads.messages.create(
                empty_thread.id,
                role="user",
                content=sanitized_user_message,
            )

            run = client.beta.threads.runs.create(
            thread_id=empty_thread.id,
            assistant_id=ASS_ID
            )

            while True:
                run_status = client.beta.threads.runs.retrieve(
                    thread_id=empty_thread.id,
                    run_id=run.id
                )
                if run_status.status == "completed":
                    break
                elif run_status.status == "failed":
                    raise Exception("Run failed.")
                time.sleep(1)

            gpt_messages = client.beta.threads.messages.list(thread_id=empty_thread.id)

            for message in gpt_messages.data:
                if message.role == "assistant":
                    ready_message = message

        except Exception as ex:
            print(ex)
    
    sanitized_text = bleach.clean(
        ready_message.content[0].text.value,
        tags=[],
        attributes={},
        strip=True
    )
        
    return ChatResponse(
        response=sanitized_text,
        message_id="placeholder-message-id",
        timestamp=datetime.now()
    )

@router.get("/history", response_model=ChatHistoryResponse)
async def get_chat_history(current_user: str = Depends(get_current_user), limit: int = 50, offset: int = 0):
    """
    Get user's conversation history
    """
    # TODO: Implement chat history logic
    # - Use current_user (user ID from JWT token)
    # - Fetch conversation history from database
    # - Apply pagination (limit, offset)
    # - Return conversations
    mock_conversations = [
        ConversationHistory(
            id="conv-1",
            user_message="What does my insurance cover?",
            ai_response="Your insurance covers basic healthcare services...",
            timestamp=datetime.now()
        ),
        ConversationHistory(
            id="conv-2",
            user_message="How do I claim reimbursement?",
            ai_response="To claim reimbursement, you need to...",
            timestamp=datetime.now()
        )
    ]
    return ChatHistoryResponse(
        conversations=mock_conversations,
        total_count=len(mock_conversations)
    )
