import asyncio
from datetime import datetime, timezone
from uuid import uuid4

from bson import ObjectId
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status

from app.core.config import get_settings
from app.core.database import get_database
from app.schemas.document import DocumentResponse, UploadResponse
from app.services.chunk_service import chunk_text
from app.services.embedding_service import embed_texts
from app.services.pdf_service import extract_pdf_pages_async, read_upload_file
from app.services.pinecone_service import get_index
from app.utils.dependencies import get_current_user

router = APIRouter(prefix='/documents', tags=['documents'])


@router.get('', response_model=list[DocumentResponse])
async def list_documents(current_user: dict = Depends(get_current_user)):
    db = get_database()
    docs = (
        await db.documents.find({'user_id': current_user['id']}).sort('created_at', -1).to_list(length=200)
    )
    return [
        DocumentResponse(
            id=str(doc['_id']),
            name=doc['name'],
            created_at=doc['created_at'],
            page_count=doc.get('page_count', 0),
            chunk_count=doc.get('chunk_count', 0),
        )
        for doc in docs
    ]


@router.post('/upload', response_model=UploadResponse)
async def upload_documents(
    files: list[UploadFile] = File(...),
    current_user: dict = Depends(get_current_user),
):
    settings = get_settings()
    db = get_database()
    index = get_index()

    uploaded: list[DocumentResponse] = []

    for file in files:
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Only PDF files are supported. Invalid file: {file.filename}',
            )

        content = await read_upload_file(file)
        pages = await extract_pdf_pages_async(content)
        if not pages:
            continue

        chunks_payload: list[dict] = []
        for page in pages:
            chunks = chunk_text(
                text=page['text'],
                chunk_size_words=settings.chunk_size_words,
                overlap_words=settings.chunk_overlap_words,
            )
            for chunk in chunks:
                chunks_payload.append(
                    {
                        'text': chunk,
                        'page_number': page['page_number'],
                    }
                )

        if not chunks_payload:
            continue

        chunk_texts = [item['text'] for item in chunks_payload]
        embeddings = await embed_texts(chunk_texts)

        now = datetime.now(timezone.utc)
        doc_obj = {
            'user_id': current_user['id'],
            'name': file.filename,
            'created_at': now,
            'page_count': len(pages),
            'chunk_count': len(chunks_payload),
        }
        insert_result = await db.documents.insert_one(doc_obj)
        doc_id = str(insert_result.inserted_id)

        vectors = []
        for i, (chunk, embedding) in enumerate(zip(chunks_payload, embeddings)):
            vector_id = f"{current_user['id']}-{doc_id}-{i}-{uuid4().hex[:8]}"
            vectors.append(
                {
                    'id': vector_id,
                    'values': embedding,
                    'metadata': {
                        'text': chunk['text'],
                        'document_id': doc_id,
                        'document_name': file.filename,
                        'page_number': chunk['page_number'],
                        'user_id': current_user['id'],
                    },
                }
            )

        batch_size = 100
        # Pinecone recommends batching writes to reduce request overhead.
        for i in range(0, len(vectors), batch_size):
            batch = vectors[i : i + batch_size]
            await asyncio.to_thread(index.upsert, vectors=batch)

        await db.documents.update_one(
            {'_id': ObjectId(doc_id)},
            {'$set': {'vector_ids': [v['id'] for v in vectors]}},
        )

        uploaded.append(
            DocumentResponse(
                id=doc_id,
                name=file.filename,
                created_at=now,
                page_count=len(pages),
                chunk_count=len(chunks_payload),
            )
        )

    return UploadResponse(documents=uploaded)


@router.delete('/{document_id}')
async def delete_document(document_id: str, current_user: dict = Depends(get_current_user)):
    db = get_database()
    index = get_index()

    try:
        oid = ObjectId(document_id)
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid document id') from exc

    doc = await db.documents.find_one({'_id': oid, 'user_id': current_user['id']})
    if doc is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Document not found')

    vector_ids: list[str] = doc.get('vector_ids', [])
    if vector_ids:
        await asyncio.to_thread(index.delete, ids=vector_ids)

    await db.documents.delete_one({'_id': oid})
    return {'status': 'deleted', 'document_id': document_id}
