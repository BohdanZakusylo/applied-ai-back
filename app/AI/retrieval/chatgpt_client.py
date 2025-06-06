# ITH-87 & ITH-89: Connect pinecone storage to ChatGPT environment  
# OpenAI ChatGPT API integration

import os
from typing import List, Dict
from openai import OpenAI
from dotenv import load_dotenv
from ..config.ai_config import AIConfig

class ChatGPTClient:
    """
    Handles ChatGPT API interactions
    """
    
    def __init__(self):
        load_dotenv()
        api_key = AIConfig.OPENAI_API_KEY
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        self.client = OpenAI(api_key=api_key)
        self.model = AIConfig.OPENAI_MODEL
    
    def generate_response(self, query: str, context_documents: List[Dict]) -> str:
        """
        Generate response using ChatGPT with RAG context
        
        Args:
            query: User question
            context_documents: Retrieved documents for context
            
        Returns:
            Generated response text
        """
        try:
            # Extract text content from context documents
            context_texts = []
            for doc in context_documents:
                if 'metadata' in doc and 'text' in doc['metadata']:
                    context_texts.append(doc['metadata']['text'])
                elif 'text' in doc:
                    context_texts.append(doc['text'])
            
            # Create context string
            context = "\n\n".join(context_texts) if context_texts else ""
            
            # Create the prompt
            prompt = self.create_prompt(query, context)
            
            # Call ChatGPT
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self._get_system_prompt()},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,  # Low temperature for factual responses
                max_tokens=500
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Error generating ChatGPT response: {e}")
            return "I'm sorry, I encountered an error while processing your request. Please try again."
    
    def create_prompt(self, query: str, context: str) -> str:
        """
        Create prompt with context for ChatGPT
        
        Args:
            query: User question
            context: Retrieved document context
            
        Returns:
            Formatted prompt
        """
        if context:
            return f"""Based on the following Dutch insurance information, please answer the user's question:

CONTEXT:
{context}

USER QUESTION:
{query}

Please provide a helpful and accurate answer based on the context provided. If the context doesn't contain enough information to answer the question, say so clearly."""
        else:
            return f"""I don't have specific insurance document context for this question, but I'll do my best to help:

USER QUESTION:
{query}

Please note that for specific insurance questions, it's best to consult your actual insurance documents or contact your provider directly."""
    
    def _get_system_prompt(self) -> str:
        """
        Get the system prompt for the Dutch insurance assistant
        
        Returns:
            System prompt string
        """
        return """You are MediWay, an AI assistant specialized in Dutch health insurance for international students. 

Your responsibilities:
- Answer questions about Dutch health insurance (zorgverzekering)
- Explain insurance terms and coverage
- Help with understanding insurance documents
- Provide guidance on medical care in the Netherlands

Guidelines:
- Always base your answers on the provided context when available
- Be clear and helpful in your explanations
- If you're unsure about something, recommend consulting official sources
- Use simple language to explain complex insurance terms
- Focus specifically on Dutch healthcare and insurance matters""" 