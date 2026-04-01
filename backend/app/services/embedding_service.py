import asyncio
from functools import lru_cache

from sentence_transformers import SentenceTransformer

from app.core.config import get_settings


@lru_cache
def get_sentence_transformer() -> SentenceTransformer:
    settings = get_settings()
    return SentenceTransformer(settings.embedding_model)


def _embed_texts(texts: list[str]) -> list[list[float]]:
    model = get_sentence_transformer()
    vectors = model.encode(texts, normalize_embeddings=True)
    return [vector.tolist() for vector in vectors]


async def embed_texts(texts: list[str]) -> list[list[float]]:
    return await asyncio.to_thread(_embed_texts, texts)


async def embed_query(query: str) -> list[float]:
    vectors = await embed_texts([query])
    return vectors[0]
