# ITH-86: Create the pinecone storage
# Pinecone client initialization and connection management

import os
from typing import Optional
from pinecone import Pinecone
from dotenv import load_dotenv 

class PineconeClient:
    """
    Handles Pinecone vector database connections and operations
    """
    
    def __init__(self):
        self.client = None
        self.index = None
        self.index_name = None
    
    def initialize_pinecone(self) -> bool:
        """
        Initialize Pinecone connection and connect to index
        - Load API key from environment
        - Set up Pinecone client
        - Connect to existing index or create if needed
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            load_dotenv()
            api_key = os.getenv("PINECONE_API_KEY")
            self.index_name = os.getenv("PINECONE_INDEX_NAME")
            
            if not api_key or not self.index_name:
                print("Missing PINECONE_API_KEY or PINECONE_INDEX_NAME in environment")
                return False
            
            # Initialize Pinecone client
            self.client = Pinecone(api_key=api_key)
            
            # Check if index exists, create if not
            existing_indexes = [index.name for index in self.client.list_indexes()]
            
            if self.index_name not in existing_indexes:
                success = self.create_index(self.index_name)
                if not success:
                    return False
            
            # Connect to the index
            self.index = self.client.Index(self.index_name)
            return True
            
        except Exception as e:
            print(f"Error initializing Pinecone: {e}")
            return False
    
    def create_index(self, index_name: str, dimension: int = 1536) -> bool:
        """
        Create new Pinecone index
        
        Args:
            index_name: Name of the index
            dimension: Vector dimension (1536 for OpenAI embeddings)
            
        Returns:
            bool: True if created successfully
        """
        try:
            if not self.client:
                print("Pinecone client not initialized")
                return False
                
            self.client.create_index(
                name=index_name,
                dimension=dimension,
                metric="cosine",
                spec={
                    "serverless": {
                        "cloud": "aws",
                        "region": "us-west-2"
                    }
                }
            )
            print(f"Successfully created index: {index_name}")
            return True
            
        except Exception as e:
            print(f"Error creating index: {e}")
            return False
    
    def get_index(self, index_name: Optional[str] = None):
        """
        Get existing Pinecone index
        
        Args:
            index_name: Name of the index (optional, uses default if not provided)
            
        Returns:
            Pinecone index object
        """
        if index_name:
            return self.client.Index(index_name) if self.client else None
        return self.index