# AI Configuration
# Environment variables and configuration settings

import os
from typing import Optional
from dotenv import load_dotenv

class AIConfig:
    """
    Configuration for AI components
    """

    load_dotenv();
    
    # OpenAI Configuration
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4")
    
    # Pinecone Configuration  
    PINECONE_API_KEY: Optional[str] = os.getenv("PINECONE_API_KEY")
    PINECONE_ENVIRONMENT: Optional[str] = os.getenv("PINECONE_ENVIRONMENT")
    PINECONE_INDEX_NAME: str = os.getenv("PINECONE_INDEX_NAME", "nl-insurance")
    
    # RAG Configuration
    CHUNK_SIZE: int = int(os.getenv("CHUNK_SIZE", "1000"))
    CHUNK_OVERLAP: int = int(os.getenv("CHUNK_OVERLAP", "200"))
    TOP_K_DOCUMENTS: int = int(os.getenv("TOP_K_DOCUMENTS", "5"))
    
    # Security Configuration
    RATE_LIMIT_PER_MINUTE: int = int(os.getenv("RATE_LIMIT_PER_MINUTE", "10"))
    MAX_MESSAGE_LENGTH: int = int(os.getenv("MAX_MESSAGE_LENGTH", "1000"))

def validate_config() -> bool:
    """
    TODO: Validate that all required configuration is present
    
    Returns:
        True if configuration is valid
    """
    required_vars = [
        AIConfig.OPENAI_API_KEY,
        AIConfig.PINECONE_API_KEY,
        AIConfig.PINECONE_ENVIRONMENT
    ]
    return all(var is not None for var in required_vars) 