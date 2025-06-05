# ITH-86: Create the pinecone storage
# Pinecone client initialization and connection management

import os
from typing import Optional
import os 
from pinecone import Pinecone
from dotenv import load_dotenv 
class PineconeClient:
    """
    Handles Pinecone vector database connections and operations
    """
    
    def __init__(self):
        # TODO: Initialize Pinecone client with API key and environment
        self.client = None
        self.index = None
        # ^ you set those up below
    
    def initialize_pinecone(self) -> bool:
        """
        TODO: Initialize Pinecone connection
        - Load API key from environment
        - Set up Pinecone environment
        - Create or connect to index
        
        Returns:
            bool: True if successful, False otherwise
        """
        try :
            load_dotenv()
            api_key = os.getenv("PINECONE_API_KEY")
            environment = os.getenv("PINECONE_ENVIRONMENT")
            index_name = os.getenv("PINECONE_INDEX_NAME")
         
            self.client = Pinecone(api_key=api_key, environment=environment)
            return True
        except : 
            return False
    def create_index(self, index_name: str, dimension: int = 1536) -> bool:
        """
        TODO: Create new Pinecone index
        
        Args:
            index_name: Name of the index
            dimension: Vector dimension (1536 for OpenAI embeddings)
            
        Returns:
            bool: True if created successfully
        """
        try :
            index_name = os.getenv("PINECONE_INDEX_NAME") 
            if index_name not in self.client.has_index(index_name): 
                self.client.create_index(name=index_name, dimension=1536, metric="cosine",cloud="aws",region="us-east-1") 
        except Exception as e:
            print(f"Error creating index: {e}")
            return False
    
    def get_index(self, index_name: str):
        """
        TODO: Get existing Pinecone index
        
        Args:
            index_name: Name of the index
            
        Returns:
            Pinecone index object
        """
        return self.index