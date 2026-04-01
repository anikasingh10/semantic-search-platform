from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.core.config import get_settings

_client: AsyncIOMotorClient | None = None


def get_client() -> AsyncIOMotorClient:
    global _client
    if _client is None:
        settings = get_settings()
        _client = AsyncIOMotorClient(settings.mongodb_uri)
    return _client


def get_database() -> AsyncIOMotorDatabase:
    settings = get_settings()
    return get_client()[settings.mongodb_db]


async def ensure_indexes() -> None:
    db = get_database()
    await db.users.create_index('email', unique=True)
    await db.documents.create_index([('user_id', 1), ('created_at', -1)])
    await db.query_history.create_index([('user_id', 1), ('created_at', -1)])
