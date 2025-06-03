from fastapi import APIRouter, HTTPException, status, Depends
from app.models.chat import (
    ChatMessage, 
    ChatResponse, 
    ChatHistoryResponse, 
    ConversationHistory, 
    ChatStatusResponse
)
from app.dependencies import get_current_user
from app.AI.integration.rag_service import RAGService
from datetime import datetime

router = APIRouter(prefix="/chat", tags=["Chat"])

# ITH-94: Integrate trained ChatpGPT with API
rag_service = RAGService()

@router.post("/message", response_model=ChatResponse)
async def send_message(message: ChatMessage, current_user: str = Depends(get_current_user)):
    """
    Send message to AI assistant and get response
    ITH-94: Integrated with RAG pipeline for insurance-specific answers
    """
    try:
        # ITH-94: Process message through RAG pipeline
        ai_response = rag_service.process_query(current_user, message.content)
        
        # TODO: Save conversation to database
        
        return ChatResponse(
            response=ai_response.get("answer", "I'm sorry, I couldn't process your request."),
            message_id=ai_response.get("message_id", "generated-id"),
            timestamp=datetime.now()
        )
    except Exception as e:
        # Fallback to placeholder if AI fails
        return ChatResponse(
            response=f"This is a placeholder response from the AI assistant regarding Dutch insurance matters for user {current_user}.",
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

@router.delete("/history", response_model=ChatStatusResponse)
async def clear_chat_history(current_user: str = Depends(get_current_user)):
    """
    Clear user's conversation history
    """
    # TODO: Implement clear history logic
    # - Use current_user (user ID from JWT token)
    # - Delete all conversations for user
    # - Return success message
    return ChatStatusResponse(message=f"Chat history cleared successfully for user {current_user}") 