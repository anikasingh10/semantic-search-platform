from pydantic import BaseModel, Field


class SearchRequest(BaseModel):
    query: str = Field(min_length=2)
    top_k: int | None = None


class SearchResult(BaseModel):
    text: str
    score: float
    document_name: str
    page_number: int


class SearchResponse(BaseModel):
    query: str
    results: list[SearchResult]
