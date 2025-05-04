from pydantic import BaseModel, EmailStr
from typing import Optional

class OrganizationCreate(BaseModel):
    name: str
    logo: Optional[str] = None
    description: Optional[str] = None

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    is_admin: bool = False

class UserOut(BaseModel):
    id: int
    email: EmailStr
    is_superadmin: bool
    is_admin: bool
    organization_id: Optional[int]

    class Config:
        orm_mode = True
