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
    Expense,
    ExpenseCreate,
    ExpenseCreatResult,
    ExpenseSuccessResult,
    ExpenseUpdate,
)

router = APIRouter(
    prefix="/v1/expenses",
    tags=["expenses"],
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Unauthorized",
            "model": GenericException,
        }
    },
)

security = HTTPBearer()


@router.get("", response_model=list[Expense])
async def get_expenses(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    user_id: Annotated[None | str, Depends(validate_access)],
) -> list[Expense]:
    """
    Get gas expenses.
    """
    results = []
    async for doc in db.expenses.find():

        updated_at = doc.get("updated_at")
        if updated_at:
            updated_at = updated_at.isoformat()

        results.append(
            Expense(
                id=str(doc.get("_id")),
                user_id=str(doc.get("_id")),
                total=doc.get("total"),
                category=doc.get("total"),
                place=doc.get("place"),
                updated_at=updated_at,
                created_at=doc.get("created_at").isoformat(),
            )
        )

    return results


@router.get(
    "/{expense_id}",
    response_model=Expense,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "Invalid expense id format.",
            "model": GenericException,
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Expense not found.",
            "model": GenericException,
        },
    },
)
async def get_expense(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    user_id: Annotated[None | str, Depends(validate_access)],
    expense_id: str,
) -> Expense:
    """
    Get a gas expense.
    """
    try:
        expense_object_id = ObjectId(expense_id)
    except bson.errors.InvalidId:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid expense id format."
        )

    doc = await db.expenses.find_one({"_id": expense_object_id})
    if not doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found."
        )

    updated_at = doc.get("updated_at")
    if updated_at:
        updated_at = updated_at.isoformat()
    return Expense(
        id=str(doc.get("_id")),
        user_id=str(doc.get("_id")),
        total=doc.get("total"),
        category=doc.get("total"),
        place=doc.get("place"),
        updated_at=updated_at,
        created_at=doc.get("created_at").isoformat(),
    )


@router.post(
    "",
    response_model=ExpenseCreatResult,
)
async def add_expense(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    user_id: Annotated[None | str, Depends(validate_access)],
    new_expense: ExpenseCreate,
) -> ExpenseCreatResult:
    """
    Add a gas expense.
    """

    data = new_expense.model_dump() | {"created_at": datetime.now(timezone.utc)}
    create_result = await db.expenses.insert_one(data)

    return ExpenseCreatResult(id=str(create_result.inserted_id))


@router.delete(
    "/{expense_id}",
    response_model=ExpenseSuccessResult,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "Invalid expense id format",
            "model": GenericException,
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Expense not found",
            "model": GenericException,
        },
    },
)
async def delete_expense(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    user_id: Annotated[None | str, Depends(validate_access)],
    expense_id: str,
) -> ExpenseSuccessResult:
    """
    Delete gas expense.
    """

    try:
        expense_object_id = ObjectId(expense_id)
    except bson.errors.InvalidId:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid expense id format."
        )

    delete_result = await db.expenses.delete_one({"_id": expense_object_id})
    if delete_result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found",
        )

    return ExpenseSuccessResult(success=True)


@router.patch(
    "/{expense_id}",
    response_model=ExpenseSuccessResult,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "Invalid expense id format, No changes provided",
            "model": GenericException,
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Expense not found.",
            "model": GenericException,
        },
    },
)
async def update_expense(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    user_id: Annotated[None | str, Depends(validate_access)],
    expense_id: str,
    expense_update: ExpenseUpdate,
) -> ExpenseSuccessResult:
    """
    Update gas expense.
    """

    try:
        expense_object_id = ObjectId(expense_id)
    except bson.errors.InvalidId:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid expense id format."
        )

    update_data = expense_update.model_dump(exclude_unset=True) | {
        "updated_at": datetime.now(timezone.utc)
    }
    update_result = await db.expenses.update_one(
        {"_id": expense_object_id}, {"$set": update_data}
    )

    if update_result.matched_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found."
        )

    return ExpenseSuccessResult(success=True)
