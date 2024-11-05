from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Expense(BaseModel):
    id: str
    user_id: str
    total: float
    category: str
    place: str
    created_at: datetime
    updated_at: Optional[datetime] = None


class ExpenseCreate(BaseModel):
    total: float
    category: str
    place: str


class ExpenseUpdate(BaseModel):
    total: Optional[float] = None
    category: Optional[str] = None
    place: Optional[str] = None


class ExpenseCreatResult(BaseModel):
    id: str


class ExpenseSuccessResult(BaseModel):
    success: bool
