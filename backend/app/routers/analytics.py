from fastapi import APIRouter, Depends

from app.core.database import get_database
from app.services.query_service import QueryService
from app.utils.dependencies import get_current_user

router = APIRouter(prefix='/analytics', tags=['analytics'])


@router.get('')
async def get_analytics(current_user: dict = Depends(get_current_user)):
    db = get_database()
    doc_count = await db.documents.count_documents({'user_id': current_user['id']})
    query_count = await QueryService.get_query_count(current_user['id'])
    return {'document_count': doc_count, 'query_count': query_count}
