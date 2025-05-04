from pydantic import BaseModel, EmailStr
from typing import Optional

# -------- Organization Schemas --------
class OrganizationCreate(BaseModel):
    name: str
    logo: Optional[str] = None
    description: Optional[str] = None

class OrganizationUpdate(BaseModel):
    name: Optional[str] = None
    logo: Optional[str] = None
    description: Optional[str] = None

class OrganizationOut(BaseModel):
    id: int
    name: str
    logo: Optional[str] = None
    description: Optional[str] = None

    class Config:
        orm_mode = True

# -------- User Schemas --------
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    is_admin: bool = False

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    is_admin: Optional[bool] = None

class UserOut(BaseModel):
    id: int
    email: EmailStr
    is_superadmin: bool
    is_admin: bool
    organization_id: Optional[int]

    class Config:
        orm_mode = True
