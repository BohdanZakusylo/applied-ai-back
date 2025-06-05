# AI Module Layout - MediWay Healthcare Assistant

## Overview
This folder contains the RAG (Retrieval-Augmented Generation) system that connects Pinecone vector storage with ChatGPT API for healthcare insurance queries.

## Folder Structure & Jira Task Mapping

### 📁 `storage/` - ITH-86: Create the pinecone storage
- `pinecone_client.py` - Pinecone initialization and connection
- `embeddings.py` - Document embedding functionality

### 📁 `documents/` - ITH-90: Make the document loader and splitter
- `loader.py` - PDF/document loading
- `splitter.py` - Text chunking and splitting
- `data_divider.py` - ITH-91: Divide the data into 6 equal parts

### 📁 `retrieval/` - ITH-87 & ITH-89: Connect pinecone storage to ChatGPT environment  
- `retriever.py` - RAG retrieval logic
- `chatgpt_client.py` - OpenAI API integration

### 📁 `security/` - ITH-85: Improve chat-bot security
- `security.py` - Security measures for chat interactions

### 📁 `data/` - ITH-93: Fill in the pinecone with data
- `data_ingestion.py` - Data processing and uploading to Pinecone

### 📁 `integration/` - ITH-87 & ITH-89: Connect pinecone storage to ChatGPT environment
- `rag_service.py` - Complete RAG pipeline that connects Pinecone to ChatGPT

### 📁 `../routers/` - ITH-94: Integrate trained ChatGPT with API
- `chat.py` - FastAPI endpoints for chat functionality

### 📁 `config/`
- `ai_config.py` - Environment variables and configuration

## Usage Flow
1. Documents loaded and processed (`documents/`)
2. Data embedded and stored in Pinecone (`storage/`)
3. User queries processed through RAG pipeline (`retrieval/`)
4. Responses generated with ChatGPT (`integration/`)
5. Security measures applied (`security/`)

## Dependencies
See main `requirements.txt` for:
- `openai`
- `pinecone-client` 
- `langchain`
- `tiktoken`
- `python-dotenv` 

## ITH-94: Integrate trained ChatGPT with API
**Note:** ITH-94 involves integrating the `RAGService` into the existing `app/routers/chat.py` endpoints, not creating new endpoints. 