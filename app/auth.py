from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

security = HTTPBearer()


async def validate_access(
    access_token: Annotated[HTTPAuthorizationCredentials, Depends(security)]
) -> str | None:
    """
    Validates access tokens.

    Raises a 401 HTTPException if an invalid token is provided.
    """

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
