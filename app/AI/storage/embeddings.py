# ITH-86: Create the pinecone storage  
# Document embedding functionality

from typing import List, Dict

class DocumentEmbedder:
    """
    Handles document embedding using OpenAI embeddings
    """
    
    def __init__(self):
        # TODO: Initialize OpenAI embeddings client
        self.embeddings_client = None
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        TODO: Convert text documents to vector embeddings
        
        Args:
            texts: List of text chunks to embed
            
        Returns:
            List of embedding vectors
        """
        pass
    
    def embed_query(self, query: str) -> List[float]:
        """
        TODO: Convert user query to vector embedding
        
        Args:
            query: User question text
            
        Returns:
            Query embedding vector
        """
        pass 