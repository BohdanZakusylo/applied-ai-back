# ITH-90: Make the document loader and splitter
# Text chunking and splitting functionality

from typing import List

class DocumentSplitter:
    """
    Splits documents into smaller chunks for embedding
    """
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        # TODO: Initialize splitter with chunk size and overlap
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def split_documents(self, documents: List[str]) -> List[str]:
        """
        TODO: Split documents into chunks
        
        Args:
            documents: List of document texts
            
        Returns:
            List of text chunks
        """
        pass
    
    def split_text(self, text: str) -> List[str]:
        """
        TODO: Split single text into chunks
        
        Args:
            text: Text to split
            
        Returns:
            List of text chunks
        """
        pass 