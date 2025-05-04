from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from models.user import User
from schemas import UserCreate, UserOut
from auth import get_password_hash
from database import async_session
from sqlalchemy.future import select

router = APIRouter()

async def get_db():
    async with async_session() as session:
        yield session

@router.post("/")
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await db.execute(select(User).where(User.email == user.email))
    if db_user.scalar():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_user = User(
        email=user.email,
        hashed_password=get_password_hash(user.password),
        is_admin=user.is_admin,
        is_superadmin=False
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

@router.get("/", response_model=list[UserOut])
async def list_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))
    return result.scalars().all()
