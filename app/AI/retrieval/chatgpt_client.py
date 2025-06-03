# ITH-87 & ITH-89: Connect pinecone storage to ChatGPT environment  
# OpenAI ChatGPT API integration

from typing import List, Dict

class ChatGPTClient:
    """
    Handles ChatGPT API interactions
    """
    
    def __init__(self):
        # TODO: Initialize OpenAI client
        self.client = None
        self.model = "gpt-4"
    
    def generate_response(self, query: str, context_documents: List[Dict]) -> str:
        """
        TODO: Generate response using ChatGPT with RAG context
        
        Args:
            query: User question
            context_documents: Retrieved documents for context
            
        Returns:
            Generated response text
        """
        pass
    
    def create_prompt(self, query: str, context: str) -> str:
        """
        TODO: Create prompt with context for ChatGPT
        
        Args:
            query: User question
            context: Retrieved document context
            
        Returns:
            Formatted prompt
        """
        pass 