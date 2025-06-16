# ITH-86: Create the pinecone storage  
# Document embedding functionality

import os
from typing import List, Dict
from openai import OpenAI
from dotenv import load_dotenv
from ..config.ai_config import AIConfig

class DocumentEmbedder:
    """
    Handles document embedding using OpenAI embeddings
    """
    
    def __init__(self):
        load_dotenv()
        api_key = AIConfig.OPENAI_API_KEY
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        self.client = OpenAI(api_key=api_key)
        self.model = "text-embedding-ada-002"  # 1536 dimensions
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        Convert text documents to vector embeddings
        
        Args:
            texts: List of text chunks to embed
            
        Returns:
            List of embedding vectors
        """
        try:
            # OpenAI API can handle multiple texts at once
            response = self.client.embeddings.create(
                input=texts,
                model=self.model
            )
            
            # Extract embeddings from response
            embeddings = [data.embedding for data in response.data]
            return embeddings
            
        except Exception as e:
            print(f"Error embedding documents: {e}")
            return []
    
    def embed_query(self, query: str) -> List[float]:
        """
        Convert user query to vector embedding
        
        Args:
            query: User question text
            
        Returns:
            Query embedding vector
        """
        try:
            response = self.client.embeddings.create(
                input=[query],
                model=self.model
            )
            
            return response.data[0].embedding
            
        except Exception as e:
            print(f"Error embedding query: {e}")
            return [] 