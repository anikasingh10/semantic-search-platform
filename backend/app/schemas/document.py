from datetime import datetime

from pydantic import BaseModel


class DocumentResponse(BaseModel):
    id: str
    name: str
    created_at: datetime
    page_count: int
    chunk_count: int


class UploadResponse(BaseModel):
    documents: list[DocumentResponse]
