# Chat Service
# This module will contain chat/AI-related business logic

import asyncio
from fastapi import HTTPException, status
from app.orm.models.db_user import User
from app.orm.models.chat import Chat
from app.orm.models.message import Message
from app.orm.engine import SessionLocal
from app.orm.db_functions.get_user_instance import decorator_get_user_instance

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
    
    @staticmethod
    @decorator_get_user_instance
    def saveNewChat(user: User, db, name: str):
        chat = Chat(name=name)
        user.chats.append(chat)
        db.add(chat)
        db.commit()
        db.refresh(chat)
        db.close()

    @staticmethod
    def get_chat_by_name(id: int, chat_name):
        session = SessionLocal()
        try:
            chat = session.query(Chat).filter_by(user_id=id, name=chat_name).first()

            return chat
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal error gettign the chat"
            )
        finally:
            session.close()

    
    @staticmethod
    def addMessageToDb(id: int, chat_name: str, message: str, isIncoming: bool):
        db = SessionLocal()
        try:
            chat = db.query(Chat).filter_by(user_id=id, name=chat_name).first()
            new_message = Message(
                message=message,
                isIncoming=isIncoming
            )
            chat.messages.append(new_message)
            db.add(new_message)
            db.commit()
            db.refresh(new_message)

            return new_message
        except Exception as e:
            db.rollback()
            print(f"Error adding message: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to add message to chat"
            )
        finally:
            db.close()
    
    @staticmethod
    @decorator_get_user_instance
    def get_user_history(user: User, db, name: str):       
        chat = db.query(Chat).filter_by(user_id=user.id, name=name).first()

        if not chat: 
            return None

        return chat.messages;

    @staticmethod
    @decorator_get_user_instance
    def get_user_chats(user, db):
        chats = db.query(Chat).filter_by(user_id=user.id).all()

        if not chats:
            return None
        
        return [x.name for x in chats]