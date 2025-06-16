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
        prompt_template = f"""User Profile Context:
- Insurance Provider: {user_profile.insurance_provider if user_profile.insurance_provider else "Not specified"} 
- General Practitioner: {user_profile.general_practitioner if user_profile.general_practitioner else "Not specified"}
- Medical Information: {user_profile.medical_information if user_profile.medical_information else "Not specified"}

Instructions for AI:
- Provide personalized advice based on the user's insurance provider when relevant
- Consider the user's medical information when giving health-related guidance
- Reference their GP when suggesting medical appointments or consultations
- Focus specifically on Dutch insurance matters and regulations
- If the user hasn't specified insurance details, suggest they add this information to their profile for better assistance

User Question: {user_message}"""
        
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