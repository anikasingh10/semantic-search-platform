from fastapi import APIRouter, Depends, HTTPException, status

from app.schemas.history import QueryHistoryItem, QueryHistoryResponse
from app.services.query_service import QueryService
from app.utils.dependencies import get_current_user

router = APIRouter(prefix='/history', tags=['history'])


@router.get('', response_model=QueryHistoryResponse)
async def get_history(current_user: dict = Depends(get_current_user)):
    items = await QueryService.get_history(current_user['id'])
    mapped = [
        QueryHistoryItem(
            id=str(item['_id']),
            query=item['query'],
            response=item.get('response'),
            created_at=item['created_at'],
        )
        for item in items
    ]
    return QueryHistoryResponse(items=mapped)


@router.delete('/{query_id}')
async def delete_query(query_id: str, current_user: dict = Depends(get_current_user)):
    """Delete a single query from history."""
    success = await QueryService.delete_query(current_user['id'], query_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Query not found')
    return {'message': 'Query deleted successfully'}


@router.delete('')
async def delete_all_history(current_user: dict = Depends(get_current_user)):
    """Delete all query history for the current user."""
    deleted_count = await QueryService.delete_all_history(current_user['id'])
    return {'message': f'Deleted {deleted_count} queries from history'}

