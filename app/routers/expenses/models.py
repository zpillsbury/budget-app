from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Expense(BaseModel):
    id: str
    expense: float
    created_at: datetime
    updated_at: Optional[datetime] = None


class ExpenseCreate(BaseModel):
    expense: float


class ExpenseUpdate(BaseModel):
    expense: float


class ExpenseCreatResult(BaseModel):
    id: str


class ExpenseSuccessResult(BaseModel):
    success: bool
