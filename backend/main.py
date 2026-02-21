from fastapi import FastAPI
from search import search

app = FastAPI()


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