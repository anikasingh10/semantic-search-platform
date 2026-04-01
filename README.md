# Semantic Search SaaS (Full-Stack)

Production-ready semantic search + RAG chat system for PDFs with isolated per-user knowledge spaces.

## Stack

- Frontend: Next.js App Router, Tailwind CSS, shadcn-style components, Framer Motion
- Backend: FastAPI, modular routers/services, async endpoints
- Vector DB: Pinecone
- Database: MongoDB
- AI: Sentence Transformers (`all-MiniLM-L6-v2`) or OpenAI embeddings + OpenAI chat for RAG answers

## Project Structure

```text
.
├── backend
│   ├── app
│   │   ├── core
│   │   ├── routers
│   │   ├── schemas
│   │   ├── services
│   │   └── utils
│   ├── .env.example
│   ├── requirements.txt
│   └── README.md
└── frontend
    ├── app
    ├── components
    ├── hooks
    ├── lib
    ├── .env.example
    └── README.md
```

## Features Implemented

- JWT auth (signup/login)
- Multi-PDF upload with progress
- PDF extraction (PyMuPDF)
- Semantic chunking (sentence-aware, overlap)
- Embeddings + Pinecone upsert with metadata
- Semantic search endpoint
- RAG chat endpoint with source attribution
- Query history persisted in MongoDB
- Analytics (query count, document count)
- Document deletion (removes vectors + metadata)
- Stream chat endpoint (bonus)
- Premium dark-mode dashboard UI with 3-pane layout

## Environment Variables

### Backend (`backend/.env`)

Copy `backend/.env.example` to `backend/.env` and fill:

- `SECRET_KEY`
- `MONGODB_URI`
- `PINECONE_API_KEY`
- `PINECONE_INDEX`
- `PINECONE_CLOUD`
- `PINECONE_REGION`
- `PINECONE_DIMENSION`
- Optional OpenAI:
  - `OPENAI_API_KEY`
  - `USE_OPENAI_EMBEDDINGS=true` (if using OpenAI vectors)

Note:
- `all-MiniLM-L6-v2` uses 384-dim vectors (`PINECONE_DIMENSION=384`).
- `text-embedding-3-small` uses 1536-dim vectors.

### Frontend (`frontend/.env.local`)

Copy `frontend/.env.example` to `frontend/.env.local`:

- `NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1`

## Run Locally

### 1. Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8000
```

### 2. Frontend

```bash
cd frontend
npm install
cp .env.example .env.local
npm run dev
```

### 3. Open app

- Frontend: `http://localhost:3000`
- Backend health: `http://localhost:8000/health`

## API Overview

- `POST /api/v1/auth/signup`
- `POST /api/v1/auth/login`
- `POST /api/v1/documents/upload`
- `GET /api/v1/documents`
- `DELETE /api/v1/documents/{document_id}`
- `POST /api/v1/search`
- `POST /api/v1/chat`
- `POST /api/v1/chat/stream`
- `GET /api/v1/history`
- `GET /api/v1/analytics`

## Deployment Notes

### Backend (Render/Railway)

- Use `backend/requirements.txt`
- Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Configure all env vars from `.env.example`

### Frontend (Vercel)

- Root directory: `frontend`
- Build command: `npm run build`
- Env var: `NEXT_PUBLIC_API_URL=<your-backend-url>/api/v1`
