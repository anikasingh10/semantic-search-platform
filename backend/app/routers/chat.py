import asyncio

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from app.schemas.chat import ChatRequest, ChatResponse, ChatSource
from app.services.query_service import QueryService
from app.services.rag_service import answer_with_rag
from app.utils.dependencies import get_current_user

router = APIRouter(prefix='/chat', tags=['chat'])


@router.post('', response_model=ChatResponse)
async def chat(payload: ChatRequest, current_user: dict = Depends(get_current_user)):
    answer, sources = await answer_with_rag(
        user_id=current_user['id'],
        question=payload.question,
        top_k=payload.top_k,
    )
    await QueryService.store_query(current_user['id'], payload.question, answer)

    return ChatResponse(answer=answer, sources=[ChatSource(**source) for source in sources])


@router.post('/stream')
async def stream_chat(payload: ChatRequest, current_user: dict = Depends(get_current_user)):
    answer, sources = await answer_with_rag(
        user_id=current_user['id'],
        question=payload.question,
        top_k=payload.top_k,
    )
    await QueryService.store_query(current_user['id'], payload.question, answer)

    async def token_stream():
        words = answer.split(' ')
        for word in words:
            yield f'{word} '
            await asyncio.sleep(0.01)

    return StreamingResponse(token_stream(), media_type='text/plain', headers={'X-Sources': str(sources)})
