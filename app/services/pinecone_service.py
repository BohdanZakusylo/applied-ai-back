import os 
from pinecone import Pinecone as PineconeClient
from dotenv import load_dotenv 
 
load_dotenv() 
 
# Initialize Pinecone with API key
pinecone = PineconeClient(api_key=os.environ.get("PINECONE_API_KEY"))

# from langchain.embeddings.openai import OpenAIEmbeddings 
# from langchain.vectorstores import Pinecone as PineconeVectorStore 
 
# embedding = OpenAIEmbeddings() 
# vectorstore = PineconeVectorStore.from_documents(docs, embedding, index_name=index_name)  
try:
    index_name = os.getenv("PINECONE_INDEX_NAME") 
    # Get list of existing indexes
    existing_indexes = [index.name for index in pinecone.list_indexes()]
    
    if index_name not in existing_indexes:
        # Create index with V2 API
        pinecone.create_index(
            name=index_name,
            dimension=1536,
            metric="cosine",
            spec={
                "serverless": {
                    "cloud": "aws",
                    "region": "us-west-2"  # Choose appropriate region
                }
            }
        )
except Exception as e:
    print(f"Error creating index: {e}")