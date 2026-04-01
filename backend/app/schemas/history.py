from datetime import datetime

from pydantic import BaseModel


class QueryHistoryItem(BaseModel):
    id: str
    query: str
    response: str | None = None
    created_at: datetime


class QueryHistoryResponse(BaseModel):
    items: list[QueryHistoryItem]
