from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import UploadFile, File
import shutil
from pdf_loader import extract_text_from_pdf
from search import search
from search import index_document

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Semantic Search API running"}


@app.get("/search")
def semantic_search(query: str):
    results = search(query)

    return {
        "query": query,
        "results": results
    }

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    file_location = f"backend/documents/{file.filename}"

    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    text = extract_text_from_pdf(file_location)

    index_document(text)

    return {"message": "Document indexed successfully"}