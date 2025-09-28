from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid

class OrgBase(BaseModel):
    name: str
    description: Optional[str] = None
    is_active: bool = True

class OrgCreate(OrgBase):
    pass

class OrgUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    is_active: Optional[bool]

class OrgOut(OrgBase):
    id: uuid.UUID
    created_at: datetime
    owner_user_id: uuid.UUID

    class Config:
        orm_mode = True
