from typing import Any

import firebase_admin
from firebase_admin import credentials
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.settings import settings


def get_db() -> AsyncIOMotorDatabase[Any]:
    """
    Get MongoDB
    """
    return AsyncIOMotorClient(settings.mongo_uri, tlsAllowInvalidCertificates=True)[
        "Budget-app"
    ]


db = get_db()

firebase_admin.initialize_app(
    credentials.Certificate(
        {
            "type": "service_account",
            "project_id": settings.google_project,
            "private_key": settings.google_auth_pk,
            "client_email": settings.google_auth_client_email,
            "token_uri": settings.google_auth_token_uri,
        }
    )
)
