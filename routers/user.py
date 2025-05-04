from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.user import User
from schemas import UserCreate, UserOut, UserUpdate
from auth import get_password_hash
from database import async_session

router = APIRouter()

async def get_db():
    async with async_session() as session:
        yield session

# Create User
@router.post("/add", response_model=UserOut)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == user.email))
    if result.scalar_one_or_none():
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

# List All Users
@router.get("/list", response_model=list[UserOut])
async def list_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))
    return result.scalars().all()

# Get User by ID
@router.get("/{user_id}", response_model=UserOut)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Update User
@router.put("/{user_id}", response_model=UserOut)
async def update_user(user_id: int, user_update: UserUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user_update.email is not None:
        user.email = user_update.email
    if user_update.password is not None:
        user.hashed_password = get_password_hash(user_update.password)
    if user_update.is_admin is not None:
        user.is_admin = user_update.is_admin

    await db.commit()
    await db.refresh(user)
    return user

# Delete User
@router.delete("/{user_id}")
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await db.delete(user)
    await db.commit()
    return {"detail": "User deleted successfully"}
