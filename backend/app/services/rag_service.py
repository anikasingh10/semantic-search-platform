import asyncio
from typing import Optional

import httpx

from app.core.config import get_settings
from app.services.embedding_service import embed_query
from app.services.pinecone_service import get_index


async def semantic_search(user_id: str, query: str, top_k: int | None = None) -> list[dict]:
    settings = get_settings()
    k = top_k or settings.top_k
    vector = await embed_query(query)
    index = get_index()

    search_result = await asyncio.to_thread(
        index.query,
        vector=vector,
        top_k=k,
        include_metadata=True,
        filter={'user_id': {'$eq': user_id}},
    )

    matches = getattr(search_result, 'matches', []) or []
    formatted: list[dict] = []
    for match in matches:
        md = match.metadata or {}
        formatted.append(
            {
                'text': md.get('text', ''),
                'score': float(match.score),
                'document_name': md.get('document_name', 'Unknown'),
                'page_number': int(md.get('page_number', 0)),
            }
        )
    return formatted


def _build_prompt(question: str, contexts: list[dict]) -> str:
    context_blocks = []
    for idx, c in enumerate(contexts, start=1):
        context_blocks.append(
            f"[{idx}] Source: {c['document_name']} (page {c['page_number']})\n{c['text']}"
        )

    context_text = '\n\n'.join(context_blocks)
    return (
        'You are an assistant that answers using only the provided document context. '
        'If context is insufficient, say what is missing. Provide a concise but complete answer '
        'and cite sources in [n] format where relevant.\n\n'
        f'Question:\n{question}\n\n'
        f'Context:\n{context_text}'
    )


async def _use_hf_inference(prompt: str) -> Optional[str]:
    """Call HuggingFace Inference API if key is configured."""
    settings = get_settings()
    if not settings.hf_api_key or not settings.use_hf_inference:
        return None

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(
                'https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1',
                headers={'Authorization': f'Bearer {settings.hf_api_key}'},
                json={'inputs': prompt, 'parameters': {'max_new_tokens': 500, 'temperature': 0.2}},
            )
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    return result[0].get('generated_text', '').replace(prompt, '').strip()
    except Exception:
        pass
    return None


def _generate_extractive_answer(question: str, contexts: list[dict]) -> str:
    """Generate answer by extracting and synthesizing top matched texts."""
    if not contexts:
        return 'No relevant documents found to answer your question.'

    # Build a coherent answer from the top 2-3 contexts
    answer_parts = [f'Based on your documents:\n']
    for idx, context in enumerate(contexts[:3], start=1):
        clean_text = context['text'].strip()
        answer_parts.append(
            f'[{idx}] From {context["document_name"]} (p. {context["page_number"]}):\n{clean_text}'
        )

    answer_parts.append('\n---')
    answer_parts.append('(This is an extractive answer from your document sources)')
    return '\n\n'.join(answer_parts)


async def answer_with_rag(user_id: str, question: str, top_k: int | None = None) -> tuple[str, list[dict]]:
    contexts = await semantic_search(user_id=user_id, query=question, top_k=top_k)
    if not contexts:
        return 'I could not find relevant context in your uploaded documents.', []

    prompt = _build_prompt(question, contexts)

    # Try HuggingFace Inference API if enabled
    hf_answer = await _use_hf_inference(prompt)
    if hf_answer:
        return hf_answer, contexts

    # Fall back to extractive answer generation
    answer = _generate_extractive_answer(question, contexts)
    return answer, contexts

