# ITH-90: Make the document loader and splitter
# PDF/document loading functionality

from typing import List, Dict

class DocumentLoader:
    """
    Loads insurance documents from various sources
    """
    
    def __init__(self):
        # TODO: Initialize document loaders
        self.supported_formats = ['.pdf', '.txt', '.docx']
    
    def load_documents(self, file_path: str) -> List[Dict]:
        """
        TODO: Load documents from file system
        
        Args:
            file_path: Path to documents directory
            
        Returns:
            List of loaded documents with metadata
        """
        pass
    
    def load_pdf(self, pdf_path: str) -> str:
        """
        TODO: Load single PDF file
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            Extracted text content
        """
        pass 