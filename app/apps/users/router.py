from apps.users.repository import UserRepository
from apps.users.schemas import UserCreate, UserRead
from db.session import get_session
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserRead, status_code=status.HTTP_200_OK)
async def register(payload: UserCreate, session: AsyncSession = Depends(get_session)):
    repo = UserRepository(session)
    existing = await repo.get_by_email(payload.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="email already associated with a user",
        )
    user = await repo.create(
        name=payload.name, email=payload.email, password_hash=payload.password
    )
    return user
