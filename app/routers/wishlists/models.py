from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Wishlist(BaseModel):
    id: str
    user_id: str
    total: float
    category: str
    name: str
    created_at: datetime
    updated_at: Optional[datetime] = None


class WishlistCreate(BaseModel):
    total: float
    name: str
    category: str


class WishlistUpdate(BaseModel):
    total: Optional[float] = None
    category: Optional[str] = None
    name: Optional[str] = None


class WishlistCreatResult(BaseModel):
    id: str


class WishlistSuccessResult(BaseModel):
    success: bool
