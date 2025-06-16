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
from app.services.user_service import UserService, MONTHLY_QUESTION_LIMIT

router = APIRouter(prefix="/chat", tags=["Chat"])

chatService = ChatService()
# ITH-94: Integrate trained ChatpGPT with API
rag_service = RAGService()

load_dotenv();

@router.post("/message", response_model=ChatResponse)
async def send_message(user_message: ChatMessage, current_user: str = Depends(get_current_user)):
    if(current_user):
        # Check monthly question limit before processing
        if not UserService.check_and_increment_monthly_questions(int(current_user)):
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Monthly question limit of {MONTHLY_QUESTION_LIMIT} questions exceeded. Please try again next month."
            )
        
        API_KEY = os.getenv("GPT_API_KEY")
        ASS_ID = os.getenv("ASS_ID")

        # Check if required environment variables are set
        if not API_KEY or not ASS_ID:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="AI service not properly configured"
            )

        ready_message = None
        try:
            # Fetch user profile for context
            user_profile = UserService.get_user_by_id(int(current_user))
            
            # Build enhanced prompt with user context
            prompt = ChatService.build_user_context_prompt(user_profile, user_message.message)
            
            client = OpenAI(api_key=API_KEY)

            empty_thread = client.beta.threads.create()
            sanitized_prompt = bleach.clean(
                prompt,
                tags=[],
                attributes={},
                strip=True
            )
            thread_message = client.beta.threads.messages.create(
                empty_thread.id,
                role="user",
                content=sanitized_prompt,
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
                    raise Exception("OpenAI assistant run failed")
                time.sleep(1)

            gpt_messages = client.beta.threads.messages.list(thread_id=empty_thread.id)

            for message in gpt_messages.data:
                if message.role == "assistant":
                    ready_message = message
                    break

        except Exception as ex:
            print(f"Error in chat processing: {ex}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error processing chat message: {str(ex)}"
            )
    
    # Check if we got a valid response
    if ready_message is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No response generated from AI"
        )

    # Check if the message has content
    if not ready_message.content or len(ready_message.content) == 0:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Empty response from AI"
        )
    
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

@router.get("/questions-remaining")
async def get_questions_remaining(current_user: str = Depends(get_current_user)):
    """
    Get the number of questions remaining for the current month
    """
    remaining = UserService.get_monthly_questions_remaining(int(current_user))
    return {"questions_remaining": remaining, "monthly_limit": MONTHLY_QUESTION_LIMIT}

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
