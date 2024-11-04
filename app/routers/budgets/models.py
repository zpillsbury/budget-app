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
    budget: float


class BudgetUpdate(BaseModel):
    budget: float


class BudgetCreatResult(BaseModel):
    id: str


class BudgetSuccessResult(BaseModel):
    success: bool
