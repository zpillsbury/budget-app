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
    Wishlist,
    WishlistCreate,
    WishlistCreatResult,
    WishlistSuccessResult,
    WishlistUpdate,
)

router = APIRouter(
    prefix="/v1/wishlists",
    tags=["wishlists"],
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Unauthorized",
            "model": GenericException,
        }
    },
)

security = HTTPBearer()


@router.get("", response_model=list[Wishlist])
async def get_wishlists(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    user_id: Annotated[None | str, Depends(validate_access)],
) -> list[Wishlist]:
    """
    Get gas wishlists.
    """
    results = []
    async for doc in db.wishlists.find({"user_id": user_id}):

        results.append(
            Wishlist(
                id=str(doc.get("_id")),
                user_id=doc.get("user_id"),
                total=doc.get("total"),
                category=doc.get("category"),
                name=doc.get("name"),
                updated_at=doc.get("updated_at"),
                created_at=doc.get("created_at"),
            )
        )

    return results


@router.get(
    "/{wishlist_id}",
    response_model=Wishlist,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "Invalid wishlist id format.",
            "model": GenericException,
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Wishlist not found.",
            "model": GenericException,
        },
    },
)
async def get_wishlist(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    user_id: Annotated[None | str, Depends(validate_access)],
    wishlist_id: str,
) -> Wishlist:
    """
    Get a wishlist.
    """
    try:
        wishlist_object_id = ObjectId(wishlist_id)
    except bson.errors.InvalidId:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid wishlist id format.",
        )

    doc = await db.wishlists.find_one({"_id": wishlist_object_id, "user_id": user_id})
    if not doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Wishlist not found."
        )

    return Wishlist(
        id=str(doc.get("_id")),
        user_id=doc.get("user_id"),
        total=doc.get("total"),
        category=doc.get("category"),
        name=doc.get("name"),
        updated_at=doc.get("updated_at"),
        created_at=doc.get("created_at"),
    )


@router.post(
    "",
    response_model=WishlistCreatResult,
)
async def add_wishlist(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    user_id: Annotated[None | str, Depends(validate_access)],
    new_wishlist: WishlistCreate,
) -> WishlistCreatResult:
    """
    Add a wishlist.
    """

    data = new_wishlist.model_dump() | {
        "user_id": user_id,
        "created_at": datetime.now(timezone.utc),
    }
    create_result = await db.wishlists.insert_one(data)

    return WishlistCreatResult(id=str(create_result.inserted_id))


@router.delete(
    "/{wishlist_id}",
    response_model=WishlistSuccessResult,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "Invalid wishlist id format",
            "model": GenericException,
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Wishlist not found",
            "model": GenericException,
        },
    },
)
async def delete_wishlist(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    user_id: Annotated[None | str, Depends(validate_access)],
    wishlist_id: str,
) -> WishlistSuccessResult:
    """
    Delete gas wishlist.
    """

    try:
        wishlist_object_id = ObjectId(wishlist_id)
    except bson.errors.InvalidId:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid wishlist id format.",
        )

    delete_result = await db.wishlists.delete_one(
        {"_id": wishlist_object_id, "user_id": user_id}
    )
    if delete_result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wishlist not found",
        )

    return WishlistSuccessResult(success=True)


@router.patch(
    "/{wishlist_id}",
    response_model=WishlistSuccessResult,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "Invalid wishlist id format, No changes provided",
            "model": GenericException,
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Wishlist not found.",
            "model": GenericException,
        },
    },
)
async def update_wishlist(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    user_id: Annotated[None | str, Depends(validate_access)],
    wishlist_id: str,
    wishlist_update: WishlistUpdate,
) -> WishlistSuccessResult:
    """
    Update gas wishlist.
    """

    try:
        wishlist_object_id = ObjectId(wishlist_id)
    except bson.errors.InvalidId:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid wishlist id format.",
        )

    update_data = wishlist_update.model_dump(exclude_unset=True) | {
        "updated_at": datetime.now(timezone.utc)
    }
    update_result = await db.wishlists.update_one(
        {"_id": wishlist_object_id, "user_id": user_id}, {"$set": update_data}
    )

    if update_result.matched_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Wishlist not found."
        )

    return WishlistSuccessResult(success=True)
