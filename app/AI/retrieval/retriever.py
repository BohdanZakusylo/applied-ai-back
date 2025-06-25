# ITH-87 & ITH-89: Connect pinecone storage to ChatGPT environment
# RAG retrieval logic

from typing import List, Dict
from ..storage.pinecone_client import PineconeClient
from ..storage.embeddings import DocumentEmbedder
from ..config.ai_config import AIConfig

class RAGRetriever:
    """
    Retrieves relevant documents from Pinecone for RAG pipeline
    """
    
    def __init__(self):
        self.pinecone_client = PineconeClient()
        self.embedder = DocumentEmbedder()
        self.top_k = AIConfig.TOP_K_DOCUMENTS
        self.similarity_threshold = 0.7  # Minimum similarity score
        
        # Initialize Pinecone connection
        if not self.pinecone_client.initialize_pinecone():
            raise ConnectionError("Failed to initialize Pinecone connection")
    
    def retrieve_documents(self, query: str, top_k: int = None) -> List[Dict]:
        """
        Retrieve relevant documents for query
        
        Args:
            query: User question
            top_k: Number of documents to retrieve (optional)
            
        Returns:
            List of relevant documents with scores and metadata (including text content)
        """
        try:
            # Use provided top_k or default
            k = top_k or self.top_k
            
            # Generate query embedding
            query_vector = self.embedder.embed_query(query)
            if not query_vector:
                print("Failed to generate query embedding")
                return []
            
            # Perform similarity search
            return self.similarity_search(query_vector, k)
            
        except Exception as e:
            print(f"Error retrieving documents: {e}")
            return []
    
    def similarity_search(self, query_vector: List[float], top_k: int = 5) -> List[Dict]:
        """
        Perform similarity search in Pinecone
        
        Args:
            query_vector: Query embedding vector
            top_k: Number of results
            
        Returns:
            Similar documents with scores and metadata containing actual text content
        """
        try:
            if not self.pinecone_client.index:
                print("Pinecone index not initialized")
                return []
            
            # Query Pinecone index
            response = self.pinecone_client.index.query(
                vector=query_vector,
                top_k=top_k,
                include_metadata=True,
                include_values=False  # Don't return the vectors themselves
            )
            
            # Filter results by similarity threshold
            relevant_docs = []
            for match in response.matches:
                if match.score >= self.similarity_threshold:
                    relevant_docs.append({
                        'id': match.id,
                        'score': match.score,
                        'metadata': match.metadata  # Contains 'text' field with actual content
                    })
                else:
                    print(f"Document {match.id} filtered out (score: {match.score:.3f} < {self.similarity_threshold})")
            
            print(f"Retrieved {len(relevant_docs)} relevant documents out of {len(response.matches)} total matches")
            return relevant_docs
            
        except Exception as e:
            print(f"Error performing similarity search: {e}")
            return [] 