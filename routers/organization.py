from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import async_session
from models.organization import Organization
from schemas import OrganizationCreate
from sqlalchemy.future import select

router = APIRouter()

async def get_db():
    async with async_session() as session:
        yield session

@router.post("/")
async def create_org(org: OrganizationCreate, db: AsyncSession = Depends(get_db)):
    new_org = Organization(**org.dict())
    db.add(new_org)
    await db.commit()
    await db.refresh(new_org)
    return new_org

@router.get("/")
async def list_orgs(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Organization))
    return result.scalars().all()
