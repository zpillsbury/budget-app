from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Budget(BaseModel):
    id: str
    user_id: str
    total: float
    category: str
    name: str
    created_at: datetime
    updated_at: Optional[datetime] = None


class BudgetCreate(BaseModel):
    total: float
    category: str
    name: str


class BudgetUpdate(BaseModel):
    total: Optional[float] = None
    category: Optional[str] = None
    name: Optional[str] = None


class BudgetCreatResult(BaseModel):
    id: str


class BudgetSuccessResult(BaseModel):
    success: bool
