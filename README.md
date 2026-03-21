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

---

## Architecture

### System Components

The platform consists of three main layers:

#### 1. Frontend (Next.js + React + TypeScript)

- **Purpose**: User interface for document upload and search queries
- **Technology**: Next.js 16, React 19, TypeScript, Tailwind CSS
- **Key Features**:
  - File upload interface for PDF documents
  - Search input with real-time query handling
  - Results display with responsive design
  - Loading states and error handling

#### 2. Backend API (FastAPI + Python)

- **Purpose**: RESTful API server handling document processing and search requests
- **Technology**: FastAPI, Python 3.x, Uvicorn
- **Endpoints**:
  - `GET /` - Health check
  - `GET /search?query=<text>` - Semantic search
  - `POST /upload` - PDF document upload and indexing

#### 3. Core Processing Engine

- **Document Processing** (`pdf_loader.py`):
  - PDF text extraction using PyPDF
  - Text cleaning and normalization
  - Chunking for optimal embedding size

- **Embedding Service** (`embedder.py`):
  - SentenceTransformer model (all-MiniLM-L6-v2)
  - Converts text chunks to 384-dimensional vectors

- **Vector Database** (`search.py`):
  - FAISS (Facebook AI Similarity Search) for vector indexing
  - L2 distance similarity search
  - In-memory storage with persistence capabilities

### Data Flow

1. **Document Ingestion**:

   ```
   PDF Upload → Text Extraction → Text Cleaning → Chunking → Embedding → Vector Indexing
   ```

2. **Query Processing**:
   ```
   User Query → Query Embedding → Similarity Search → Top-K Results → API Response
   ```

---

## Workflow

### User Workflow

1. **Upload Documents**: Users upload PDF files through the web interface
2. **Automatic Processing**: System extracts text, cleans it, and creates searchable embeddings
3. **Search Queries**: Users enter natural language queries
4. **Instant Results**: System returns semantically relevant text chunks

### Technical Workflow

#### Document Indexing Pipeline

```python
# 1. PDF Processing
pdf_text = extract_text_from_pdf(file_path)

# 2. Text Chunking
chunks = chunk_text(pdf_text, max_words=250)

# 3. Embedding Generation
for chunk in chunks:
    embedding = create_embedding(chunk)  # 384-dim vector
    index.add(embedding)  # Add to FAISS index
    document_chunks.append(chunk)  # Store original text
```

#### Search Pipeline

```python
# 1. Query Embedding
query_embedding = create_embedding(user_query)

# 2. Similarity Search
distances, indices = index.search(query_embedding, k=3)

# 3. Result Retrieval
results = [document_chunks[i] for i in indices[0]]
```

---

## Setup Instructions

### Prerequisites

- Python 3.8+
- Node.js 18+
- npm or yarn

### Backend Setup

1. **Navigate to backend directory**:

   ```bash
   cd backend
   ```

2. **Create virtual environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r ../requirements.txt
   ```

4. **Start the backend server**:

   ```bash
   python main.py
   ```

   The API will be available at `http://127.0.0.1:8000`

### Frontend Setup

1. **Navigate to frontend directory**:

   ```bash
   cd frontend
   ```

2. **Install dependencies**:

   ```bash
   npm install
   ```

3. **Start the development server**:

   ```bash
   npm run dev
   ```

   The frontend will be available at `http://localhost:3000`

### Usage

1. **Start both servers** (backend and frontend)
2. **Open browser** and navigate to `http://localhost:3000`
3. **Upload a PDF** using the file upload interface
4. **Enter search queries** in natural language
5. **View results** that are semantically relevant to your query

### Configuration

- **Embedding Model**: Currently uses `all-MiniLM-L6-v2` (384 dimensions)
- **Chunk Size**: 250 words maximum per chunk
- **Search Results**: Returns top 3 most similar results
- **Vector Database**: FAISS IndexFlatL2 (L2 distance)

### Development

- **Linting**: `npm run lint` (frontend)
- **Build**: `npm run build` (frontend)
- **Testing**: Add test files in respective directories

---

## API Reference

### Search Endpoint

```http
GET /search?query=<string>
```

**Response**:

```json
{
  "query": "user query",
  "results": ["result1", "result2", "result3"]
}
```

### Upload Endpoint

```http
POST /upload
Content-Type: multipart/form-data
```

**Body**: PDF file
**Response**:

```json
{
  "message": "Document indexed successfully"
}
```
