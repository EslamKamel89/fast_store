from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.apps.auth.repository import AuthRepository
from app.apps.auth.schemas import Login, TokenPair
from app.apps.users.repository import UserRepository
from app.core.security import Security
from app.db.session import get_session

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenPair)
async def login(payload: Login, session: AsyncSession = Depends(get_session)):
    user_repo = UserRepository(session)
    user = await user_repo.get_by_email(payload.email)
    if (not user) or (
        not Security.verify_password(payload.password, user.password_hash)
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong credentials"
        )
    access_token = Security.create_access_token(subject=str(user.id))
    auth_repo = AuthRepository(session)
    refresh_token = await auth_repo.create_refresh_token(user_id=user.id)  # type: ignore
    return TokenPair(access_token=access_token, refresh_token=refresh_token.token)


@router.post("/refresh", response_model=TokenPair)
async def refresh(refresh_token: str, session: AsyncSession = Depends(get_session)):
    auth_repo = AuthRepository(session)
    record = await auth_repo.get_by_token(refresh_token)
    if not record or record.revoked:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
        )
    expires_at = record.expires_at
    if expires_at is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
        )

    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)

    if expires_at < datetime.now(timezone.utc):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
        )

    access = Security.create_access_token(str(record.user_id))
    await auth_repo.revoke(record.token)
    new_rt = await auth_repo.create_refresh_token(user_id=record.user_id)
    return TokenPair(access_token=access, refresh_token=new_rt.token)


@router.post("/logout")
async def logout(refresh_token: str, session: AsyncSession = Depends(get_session)):
    auth_repo = AuthRepository(session)
    ok = await auth_repo.revoke(refresh_token)
    if not ok:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token not found"
        )
    return {"detail": "logged out"}
