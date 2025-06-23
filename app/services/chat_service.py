# Chat Service
# This module will contain chat/AI-related business logic

import asyncio
from typing import Dict, Optional
from app.orm.db_user import User

class ChatService:
    """
    Service class for handling chat operations
    """
    
    @staticmethod
    def build_user_context_prompt(user_profile: User, user_message: str) -> str:
        prompt_template = f"""User Profile:
- Insurance Provider: {user_profile.insurance_provider if user_profile.insurance_provider else "Not specified"} 
- General Practitioner: {user_profile.general_practitioner if user_profile.general_practitioner else "Not specified"}
- Medical Information: {user_profile.medical_information if user_profile.medical_information else "Not specified"}

RULES:
- Always follow the system prompt.
- Keep sentences clear and direct
- If profile incomplete (Not specified), suggest adding insurance details to their profile.
- End your response with a "Next Steps:" paragraph with specific actionable advice
- Keep track of previous questions and answers.

User Question: {user_message}

Get the answer from your vector store."""
        
        return prompt_template
        
    
    async def save_conversation(user_id: str, user_message: str, ai_response: str):
        """
        Save conversation to database
        TODO: Implement conversation storage
        """
        pass
    
    async def get_conversation_history(user_id: str, limit: int = 50, offset: int = 0):
        """
        Get user's conversation history
        TODO: Implement conversation history retrieval
        """
        pass
    
    async def clear_conversation_history(user_id: str):
        """
        Clear user's conversation history
        TODO: Implement conversation history deletion
        """
        pass
    
    async def build_context_from_history(user_id: str, limit: int = 5):
        """
        Build conversation context from recent history
        TODO: Implement context building for AI
        """
        pass 