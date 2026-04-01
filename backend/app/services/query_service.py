from datetime import datetime, timezone

from bson import ObjectId

from app.core.database import get_database


class QueryService:
    @staticmethod
    async def store_query(user_id: str, query: str, response: str | None = None) -> None:
        db = get_database()
        await db.query_history.insert_one(
            {
                'user_id': user_id,
                'query': query,
                'response': response,
                'created_at': datetime.now(timezone.utc),
            }
        )

    @staticmethod
    async def get_history(user_id: str, limit: int = 30) -> list[dict]:
        db = get_database()
        cursor = db.query_history.find({'user_id': user_id}).sort('created_at', -1).limit(limit)
        return await cursor.to_list(length=limit)

    @staticmethod
    async def get_query_count(user_id: str) -> int:
        db = get_database()
        return await db.query_history.count_documents({'user_id': user_id})

    @staticmethod
    async def delete_query(user_id: str, query_id: str) -> bool:
        """Delete a single query by id. Returns True if deleted, False if not found."""
        db = get_database()
        try:
            result = await db.query_history.delete_one({'_id': ObjectId(query_id), 'user_id': user_id})
            return result.deleted_count > 0
        except Exception:
            return False

    @staticmethod
    async def delete_all_history(user_id: str) -> int:
        """Delete all query history for a user. Returns count of deleted items."""
        db = get_database()
        result = await db.query_history.delete_many({'user_id': user_id})
        return result.deleted_count

