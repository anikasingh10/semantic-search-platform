from functools import lru_cache

from pinecone import Pinecone, ServerlessSpec

from app.core.config import get_settings


@lru_cache
def get_pinecone_client() -> Pinecone:
    settings = get_settings()
    return Pinecone(api_key=settings.pinecone_api_key)


async def ensure_index_exists() -> None:
    settings = get_settings()
    client = get_pinecone_client()

    listed = client.list_indexes()
    if hasattr(listed, 'names'):
        existing = set(listed.names())
    else:
        existing = {idx['name'] for idx in listed}
    if settings.pinecone_index not in existing:
        client.create_index(
            name=settings.pinecone_index,
            dimension=settings.pinecone_dimension,
            metric='cosine',
            spec=ServerlessSpec(cloud=settings.pinecone_cloud, region=settings.pinecone_region),
        )


def get_index():
    settings = get_settings()
    client = get_pinecone_client()
    return client.Index(settings.pinecone_index)
