from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Bill(BaseModel):
    id: str
    user_id: str
    total: float
    category: str
    place: str
    created_at: datetime
    updated_at: Optional[datetime] = None


class BillCreate(BaseModel):
    total: float
    category: str
    place: str


class BillUpdate(BaseModel):
    total: Optional[float] = None
    category: Optional[str] = None
    place: Optional[str] = None


class BillCreateResult(BaseModel):
    id: str


class BillSuccessResult(BaseModel):
    success: bool
