from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    question: str = Field(min_length=2)
    top_k: int | None = None


class ChatSource(BaseModel):
    text: str
    document_name: str
    page_number: int
    score: float


class ChatResponse(BaseModel):
    answer: str
    sources: list[ChatSource]
