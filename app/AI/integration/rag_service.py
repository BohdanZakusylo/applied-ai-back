# ITH-87 & ITH-89: Connect pinecone storage to ChatGPT environment
# Complete RAG pipeline service - connects Pinecone retrieval with ChatGPT

import uuid
from datetime import datetime
from typing import Dict, List
from ..retrieval.retriever import RAGRetriever
from ..retrieval.chatgpt_client import ChatGPTClient
from ..security.security import ChatSecurity

class RAGService:
    """
    Main service that orchestrates the complete RAG pipeline
    """
    
    def __init__(self):
        self.retriever = RAGRetriever()
        self.chatgpt_client = ChatGPTClient()
        self.security = ChatSecurity()
    
    def process_query(self, user_id: str, query: str) -> Dict:
        """
        Process user query through complete RAG pipeline
        
        Args:
            user_id: User identifier for security checks
            query: User question about insurance
            
        Returns:
            Response with answer and metadata
        """
        try:
            # Security validation
            if not self.security.validate_user_input(user_id, query):
                return {
                    "error": "Invalid input or security violation detected",
                    "answer": None,
                    "message_id": str(uuid.uuid4()),
                    "timestamp": datetime.now(),
                    "sources": []
                }
            
            # Check rate limits
            if not self.security.check_rate_limit(user_id):
                return {
                    "error": "Rate limit exceeded. Please wait before sending another message.",
                    "answer": None,
                    "message_id": str(uuid.uuid4()),
                    "timestamp": datetime.now(),
                    "sources": []
                }
            
            # Get insurance-specific answer through RAG
            answer_data = self.get_insurance_answer(query)
            
            # Sanitize response
            sanitized_answer = self.security.sanitize_response(answer_data["answer"])
            
            return {
                "answer": sanitized_answer,
                "message_id": str(uuid.uuid4()),
                "timestamp": datetime.now(),
                "sources": answer_data.get("sources", []),
                "retrieval_info": {
                    "documents_found": len(answer_data.get("sources", [])),
                    "similarity_scores": [src.get("score", 0) for src in answer_data.get("sources", [])]
                }
            }
            
        except Exception as e:
            print(f"Error processing query: {e}")
            return {
                "error": "An error occurred while processing your request",
                "answer": "I'm sorry, I encountered an error while processing your request. Please try again.",
                "message_id": str(uuid.uuid4()),
                "timestamp": datetime.now(),
                "sources": []
            }
    
    def get_insurance_answer(self, query: str) -> Dict:
        """
        Get insurance-specific answer using RAG
        
        Args:
            query: Insurance question
            
        Returns:
            Dict containing AI-generated answer with context and sources
        """
        try:
            # Step 1: Retrieve relevant documents
            print(f"Retrieving documents for query: {query[:100]}...")
            relevant_docs = self.retriever.retrieve_documents(query)
            
            if not relevant_docs:
                print("No relevant documents found, using ChatGPT without context")
                # Generate response without context
                answer = self.chatgpt_client.generate_response(query, [])
                return {
                    "answer": answer,
                    "sources": [],
                    "context_used": False
                }
            
            # Step 2: Generate response with context
            print(f"Generating response with {len(relevant_docs)} context documents")
            answer = self.chatgpt_client.generate_response(query, relevant_docs)
            
            # Step 3: Prepare source information
            sources = []
            for doc in relevant_docs:
                source_info = {
                    "id": doc.get("id", "unknown"),
                    "score": doc.get("score", 0),
                    "excerpt": self._get_document_excerpt(doc)
                }
                
                # Add source metadata if available
                if "metadata" in doc:
                    metadata = doc["metadata"]
                    source_info.update({
                        "source_file": metadata.get("source", "unknown"),
                        "category": metadata.get("category", "general")
                    })
                
                sources.append(source_info)
            
            return {
                "answer": answer,
                "sources": sources,
                "context_used": True
            }
            
        except Exception as e:
            print(f"Error getting insurance answer: {e}")
            return {
                "answer": "I'm sorry, I encountered an error while searching for relevant information. Please try rephrasing your question.",
                "sources": [],
                "context_used": False
            }
    