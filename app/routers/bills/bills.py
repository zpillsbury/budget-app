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

from .models import Bill, BillCreate, BillCreateResult, BillSuccessResult, BillUpdate

router = APIRouter(
    prefix="/v1/bills",
    tags=["bills"],
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Unauthorized",
            "model": GenericException,
        }
    },
)

security = HTTPBearer()


@router.get("", response_model=list[Bill])
async def get_bills(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    user_id: Annotated[None | str, Depends(validate_access)],
) -> list[Bill]:
    """
    Get bills
    """
    results = []
    async for doc in db.bills.find({"user_id": user_id}):

        results.append(
            Bill(
                id=str(doc.get("_id")),
                user_id=doc.get("user_id"),
                total=doc.get("total"),
                category=doc.get("category"),
                place=doc.get("place"),
                updated_at=doc.get("updated_at"),
                created_at=doc.get("created_at"),
            )
        )

    return results


@router.get(
    "/{bill_id}",
    response_model=Bill,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "Invalid bill id format.",
            "model": GenericException,
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Bill not found.",
            "model": GenericException,
        },
    },
)
async def get_bill(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    user_id: Annotated[None | str, Depends(validate_access)],
    bill_id: str,
) -> Bill:
    """
    Get a bill.
    """
    try:
        bill_object_id = ObjectId(bill_id)
    except bson.errors.InvalidId:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid bill id format."
        )

    doc = await db.bills.find_one({"_id": bill_object_id, "user_id": user_id})
    if not doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Bill not found."
        )

    return Bill(
        id=str(doc.get("_id")),
        user_id=doc.get("user_id"),
        total=doc.get("total"),
        category=doc.get("category"),
        place=doc.get("place"),
        updated_at=doc.get("updated_at"),
        created_at=doc.get("created_at"),
    )


@router.post(
    "",
    response_model=BillCreateResult,
)
async def add_bill(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    user_id: Annotated[None | str, Depends(validate_access)],
    new_bill: BillCreate,
) -> BillCreateResult:
    """
    Add a bill.
    """
    data = new_bill.model_dump() | {
        "user_id": user_id,
        "created_at": datetime.now(timezone.utc),
    }
    create_result = await db.bills.insert_one(data)
    create_result_str = str(create_result.inserted_id)

    return BillCreateResult(id=create_result_str)


@router.delete(
    "/{bill_id}",
    response_model=BillSuccessResult,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "Invalid bill id format",
            "model": GenericException,
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Bill not found",
            "model": GenericException,
        },
    },
)
async def delete_bill(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    user_id: Annotated[None | str, Depends(validate_access)],
    bill_id: str,
) -> BillSuccessResult:
    """
    Deletes a bill.
    """
    try:
        bill_object_id = ObjectId(bill_id)
    except bson.errors.InvalidId:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid bill id format."
        )

    delete_result = await db.bills.delete_one(
        {"_id": bill_object_id, "user_id": user_id}
    )
    if delete_result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bill not found",
        )

    return BillSuccessResult(success=True)


@router.patch(
    "/{bill_id}",
    response_model=BillSuccessResult,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "Invalid bill id format, No changes provided",
            "model": GenericException,
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Bill not found.",
            "model": GenericException,
        },
    },
)
async def update_bill(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    user_id: Annotated[None | str, Depends(validate_access)],
    bill_id: str,
    bill_update: BillUpdate,
) -> BillSuccessResult:
    """
    Updates a bill.
    """
    try:
        bill_object_id = ObjectId(bill_id)
    except bson.errors.InvalidId:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid bill id format."
        )

    update_data = bill_update.model_dump(exclude_unset=True) | {
        "updated_at": datetime.now(timezone.utc)
    }
    update_result = await db.bills.update_one(
        {"_id": bill_object_id, "user_id": user_id}, {"$set": update_data}
    )

    if update_result.matched_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Bill not found."
        )

    return BillSuccessResult(success=True)
