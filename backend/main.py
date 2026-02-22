from fastapi import FastAPI
from search import search
from fastapi.middleware.cors import CORSMiddleware

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