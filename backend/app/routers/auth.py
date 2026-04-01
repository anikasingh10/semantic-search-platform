from fastapi import APIRouter, HTTPException, status

from app.core.security import create_access_token
from app.schemas.auth import LoginRequest, SignupRequest, TokenResponse
from app.services.user_service import UserService

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post('/signup', response_model=TokenResponse)
async def signup(payload: SignupRequest):
    try:
        user = await UserService.create_user(
            email=payload.email,
            password=payload.password,
            full_name=payload.full_name,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    user_id = str(user['_id'])
    token = create_access_token(user_id)
    return TokenResponse(access_token=token, user_id=user_id, email=user['email'])


@router.post('/login', response_model=TokenResponse)
async def login(payload: LoginRequest):
    user = await UserService.authenticate_user(payload.email, payload.password)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid credentials')

    user_id = str(user['_id'])
    token = create_access_token(user_id)
    return TokenResponse(access_token=token, user_id=user_id, email=user['email'])
