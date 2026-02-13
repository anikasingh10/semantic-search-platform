# Semantic Search Platform (Vector DB Based)

This project implements a **Semantic Search Platform** that retrieves information based on contextual meaning instead of exact keyword matching. The system uses transformer based embeddings to convert text into vectors and stores them in a vector database. User queries are also embedded and matched using vector similarity search to return the most relevant results.

This type of system is commonly used in AI-powered document search, knowledge retrieval and RAG (Retrieval Augmented Generation) pipelines.

---

## Objective

Build an intelligent search system that:
- Understands semantic meaning of text
- Retrieves contextually relevant results
- Works even when query words differ from document words
- Performs fast similarity-based retrieval using vector indexing

---

## How It Works

1. Documents are collected and preprocessed  
2. Text is split into smaller chunks  
3. Each chunk is converted into an embedding vector using a transformer model  
4. Embeddings are stored in a vector database (FAISS / ChromaDB)  
5. User query is converted into an embedding  
6. Similarity search is performed against stored vectors  
7. Top-K most similar results are returned

---

## Core Concepts Used

- Semantic embeddings  
- Transformer models  
- Vector databases  
- Cosine similarity  
- Nearest neighbor search  
- Text chunking & preprocessing  

---

## Tech Stack

- Python  
- SentenceTransformers / HuggingFace Embeddings  
- FAISS or ChromaDB  
- FastAPI / Flask (API layer)  
- Streamlit 
- LangChain (pipeline support)

---

## Features

- Meaning-based search instead of keyword matching
- Vector embedding generation
- Fast similarity retrieval
- Scalable vector indexing
- Clean document preprocessing pipeline
- API-based query support
- Easily extendable to RAG chatbot systems
