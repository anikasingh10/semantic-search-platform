from pydantic import BaseModel, EmailStr, Field, field_validator


class SignupRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    full_name: str | None = None

    @field_validator('password')
    @classmethod
    def validate_password(cls, password: str) -> str:
        if len(password.encode('utf-8')) > 72:
            raise ValueError(
                'Password must be at most 72 bytes long. Truncate manually if necessary.'
            )
        return password


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = 'bearer'
    user_id: str
    email: EmailStr
