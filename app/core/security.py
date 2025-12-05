from datetime import datetime, timedelta, timezone
from typing import Any

from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["argon2"])


class Security:

    @classmethod
    def hash_password(cls, password: str) -> str:
        return pwd_context.hash(password)

    @classmethod
    def verify_password(cls, plain: str, hashed: str) -> bool:
        return pwd_context.verify(plain, hashed)

    @classmethod
    def create_access_token(
        cls, subject: str, extra: dict[str, Any] | None = None
    ) -> str:
        payload: dict[str, Any] = {"sub": subject}
        if extra:
            payload.update(extra)
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_EXPIRE_MINUTES
        )
        payload["exp"] = expire
        return jwt.encode(payload, key=settings.JWT_SECRET, algorithm=settings.JWT_ALG)

    # we will not use jwt refresh tokens but we will Use random string refresh tokens (with RefreshToken.create_token_str())
    # @classmethod
    # def create_refresh_token(cls, subject: str) -> str:
    #     payload: dict[str, Any] = {"sub": subject}
    #     expire = datetime.now(timezone.utc) + timedelta(
    #         days=settings.REFRESH_EXPIRE_DAYS
    #     )
    #     payload["exp"] = expire
    #     payload["refresh"] = "refresh"
    #     return jwt.encode(payload, key=settings.JWT_SECRET, algorithm=settings.JWT_ALG)

    @classmethod
    def decode_token(cls, token: str) -> dict[str, Any]:
        try:
            return jwt.decode(
                token, key=settings.JWT_SECRET, algorithms=[settings.JWT_ALG]
            )
        except Exception as e:
            raise e
