from typing import Any

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.settings import settings

db: AsyncIOMotorDatabase[Any] = AsyncIOMotorClient(
    settings.mongo_uri, tlsAllowInvalidCertificates=True
)["gas"]
