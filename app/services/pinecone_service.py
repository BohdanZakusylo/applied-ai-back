# import os 
# from pinecone import Pinecone, ServerlessSpec
# from dotenv import load_dotenv 
 
# load_dotenv() 
 
# pinecone = Pinecone(
#     api_key=os.environ.get("PINECONE_API_KEY")
# )

from langchain.embeddings.openai import OpenAIEmbeddings 
from langchain.vectorstores import Pinecone as PineconeVectorStore 
 
embedding = OpenAIEmbeddings() 
vectorstore = PineconeVectorStore.from_documents(docs, embedding, index_name=index_name)  