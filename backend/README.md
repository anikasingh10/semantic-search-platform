# Backend (FastAPI)

## Run locally

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8000
```

## API prefix

- `http://localhost:8000/api/v1`

## Key endpoints

- `POST /auth/signup`
- `POST /auth/login`
- `POST /documents/upload`
- `GET /documents`
- `DELETE /documents/{document_id}`
- `POST /search`
- `POST /chat`
- `POST /chat/stream`
- `GET /history`
- `GET /analytics`
