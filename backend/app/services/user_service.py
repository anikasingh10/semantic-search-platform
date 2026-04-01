from datetime import datetime, timezone

from pymongo.errors import DuplicateKeyError

from app.core.database import get_database
from app.core.security import get_password_hash, verify_password


class UserService:
    @staticmethod
    async def create_user(email: str, password: str, full_name: str | None = None) -> dict:
        db = get_database()
        user = {
            'email': email.lower(),
            'full_name': full_name,
            'password_hash': get_password_hash(password),
            'created_at': datetime.now(timezone.utc),
        }
        try:
            result = await db.users.insert_one(user)
        except DuplicateKeyError as exc:
            raise ValueError('Email already exists') from exc
        user['_id'] = result.inserted_id
        return user

    @staticmethod
    async def authenticate_user(email: str, password: str) -> dict | None:
        db = get_database()
        user = await db.users.find_one({'email': email.lower()})
        if not user:
            return None
        if not verify_password(password, user['password_hash']):
            return None
        return user
