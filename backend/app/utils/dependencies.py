from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from bson import ObjectId

from app.core.database import get_database
from app.core.security import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/v1/auth/login')


async def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    payload = decode_token(token)
    if not payload or 'sub' not in payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid authentication token',
            headers={'WWW-Authenticate': 'Bearer'},
        )

    user_id = payload['sub']
    db = get_database()
    user = await db.users.find_one({'_id': user_id})
    if user is None:
        try:
            user = await db.users.find_one({'_id': ObjectId(user_id)})
        except Exception:
            user = None

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='User not found',
            headers={'WWW-Authenticate': 'Bearer'},
        )

    user['id'] = str(user['_id'])
    return user
