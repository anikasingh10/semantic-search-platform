from fastapi import APIRouter, Depends

from app.schemas.search import SearchRequest, SearchResponse, SearchResult
from app.services.query_service import QueryService
from app.services.rag_service import semantic_search
from app.utils.dependencies import get_current_user

router = APIRouter(prefix='/search', tags=['search'])


@router.post('', response_model=SearchResponse)
async def search(payload: SearchRequest, current_user: dict = Depends(get_current_user)):
    results = await semantic_search(current_user['id'], payload.query, payload.top_k)
    await QueryService.store_query(current_user['id'], query=payload.query)

    mapped = [SearchResult(**result) for result in results]
    return SearchResponse(query=payload.query, results=mapped)
