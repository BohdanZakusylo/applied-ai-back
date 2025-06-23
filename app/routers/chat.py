import time
import os
import bleach

from openai import OpenAI
from fastapi import APIRouter, HTTPException, status, Depends, status, Query
from app.models.chat import (
    ChatMessage, 
    ChatResponse, 
    ChatHistoryResponse, 
    ConversationHistory, 
    NewCratedChatResponse,
    GetHistory,
    GetChats
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

            chat_existing = ChatService.get_chat_by_name(current_user, user_message.chat_name)

            if chat_existing:
                ChatService.addMessageToDb(current_user, user_message.chat_name,user_message.message, False)
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
            print(ex)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error processing chat message"
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

    if chat_existing:
          ChatService.addMessageToDb(current_user, user_message.chat_name, sanitized_text, True)
        
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

@router.post("/new-chat", response_model=NewCratedChatResponse, status_code=status.HTTP_201_CREATED)
async def create_new_chat(current_user: str = Depends(get_current_user)):
    chat_name = f"chat-{datetime.now().isoformat()}"
    ChatService.saveNewChat(user_id=current_user, name=chat_name)
    return NewCratedChatResponse(response="Chat with has been created succesfuly", chat_name=chat_name)

#delete chat

@router.get("/chats", response_model=GetChats, status_code=status.HTTP_200_OK)
async def get_all_chats(current_user: str = Depends(get_current_user)):
    chats = ChatService.get_user_chats(user_id=current_user)
    return GetChats(chat_names=chats)

@router.get("/history", response_model=ChatHistoryResponse, status_code=status.HTTP_200_OK)
async def get_chat_history(chat_name: str = Query(...), current_user: str = Depends(get_current_user)):
    messages = ChatService.get_user_history(user_id=current_user, name=chat_name)

    if not messages:
        return ChatHistoryResponse(
            conversations=[],
            message=f"No messages were found"
        )

    conversations = [
        ConversationHistory(
            id=msg.id,
            message=msg.message,
            isIncoming=msg.isIncoming,
            created_at=msg.created_at
        )
        for msg in messages
    ]

    return ChatHistoryResponse(
        conversations=conversations,
        message=f"Found {len(conversations)} messages in chat '{chat_name}'"
    )