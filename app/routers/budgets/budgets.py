from datetime import datetime, timezone
from typing import Annotated

import bson
from bson import ObjectId
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.auth import validate_access
from app.models import GenericException
from app.utilities.clients import db

from .models import (
    Budget,
    BudgetCreate,
    BudgetCreatResult,
    BudgetSuccessResult,
    BudgetUpdate,
)

router = APIRouter(
    prefix="/v1/budgets",
    tags=["budgets"],
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Unauthorized",
            "model": GenericException,
        }
    },
)

security = HTTPBearer()


@router.get("", response_model=list[Budget])
async def get_budgets(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    user_id: Annotated[None | str, Depends(validate_access)],
) -> list[Budget]:
    """
    Get gas budgets.
    """
    results = []
    async for doc in db.budgets.find():

        updated_at = doc.get("updated_at")
        if updated_at:
            updated_at = updated_at.isoformat()

        results.append(
            Budget(
                id=str(doc.get("_id")),
                user_id=doc.get("_id"),
                total=doc.get("total"),
                category=doc.get("total"),
                name=doc.get("name"),
                updated_at=updated_at,
                created_at=doc.get("created_at").isoformat(),
            )
        )

    return results


@router.get(
    "/{budget_id}",
    response_model=Budget,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "Invalid budget id format.",
            "model": GenericException,
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Budget not found.",
            "model": GenericException,
        },
    },
)
async def get_budget(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    user_id: Annotated[None | str, Depends(validate_access)],
    budget_id: str,
) -> Budget:
    """
    Get a gas budget.
    """
    try:
        budget_object_id = ObjectId(budget_id)
    except bson.errors.InvalidId:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid budget id format."
        )

    doc = await db.budgets.find_one({"_id": budget_object_id})
    if not doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Budget not found."
        )

    updated_at = doc.get("updated_at")
    if updated_at:
        updated_at = updated_at.isoformat()

    return Budget(
        id=str(doc.get("_id")),
        user_id=doc.get("_id"),
        total=doc.get("total"),
        category=doc.get("total"),
        name=doc.get("name"),
        updated_at=updated_at,
        created_at=doc.get("created_at").isoformat(),
    )


@router.post(
    "",
    response_model=BudgetCreatResult,
)
async def add_budget(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    user_id: Annotated[None | str, Depends(validate_access)],
    new_budget: BudgetCreate,
) -> BudgetCreatResult:
    """
    Add a gas budget.
    """

    data = new_budget.model_dump() | {"created_at": datetime.now(timezone.utc)}
    create_result = await db.budgets.insert_one(data)

    return BudgetCreatResult(id=str(create_result.inserted_id))


@router.delete(
    "/{budget_id}",
    response_model=BudgetSuccessResult,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "Invalid budget id format",
            "model": GenericException,
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Budget not found",
            "model": GenericException,
        },
    },
)
async def delete_budget(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    user_id: Annotated[None | str, Depends(validate_access)],
    budget_id: str,
) -> BudgetSuccessResult:
    """
    Delete gas budget.
    """

    try:
        budget_object_id = ObjectId(budget_id)
    except bson.errors.InvalidId:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid budget id format."
        )

    delete_result = await db.budgets.delete_one({"_id": budget_object_id})
    if delete_result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Budget not found",
        )

    return BudgetSuccessResult(success=True)


@router.patch(
    "/{budget_id}",
    response_model=BudgetSuccessResult,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "Invalid budget id format, No changes provided",
            "model": GenericException,
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Budget not found.",
            "model": GenericException,
        },
    },
)
async def update_budget(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    user_id: Annotated[None | str, Depends(validate_access)],
    budget_id: str,
    budget_update: BudgetUpdate,
) -> BudgetSuccessResult:
    """
    Update gas budget.
    """

    try:
        budget_object_id = ObjectId(budget_id)
    except bson.errors.InvalidId:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid budget id format."
        )

    update_data = budget_update.model_dump(exclude_unset=True) | {
        "updated_at": datetime.now(timezone.utc)
    }
    update_result = await db.budgets.update_one(
        {"_id": budget_object_id}, {"$set": update_data}
    )

    if update_result.matched_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Budget not found."
        )

    return BudgetSuccessResult(success=True)
