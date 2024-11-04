import time
from typing import Any, Callable, TypeVar

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware

from app.routers.budgets import budgets
from app.routers.expenses import expenses

from .utilities.log import logger

F = TypeVar("F", bound=Callable[..., Any])


app = FastAPI(
    title="Budget planner",
    description="We think ahead",
    version="1.0.0",
    docs_url="/",
)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:8000",
    ],
)


@app.middleware("http")
async def process_time_log_middleware(request: Request, call_next: F) -> Response:
    """
    Add API process time in response headers and log calls
    """
    start_time = time.time()
    response: Response = await call_next(request)
    process_time = str(round(time.time() - start_time, 3))
    response.headers["X-Process-Time"] = process_time

    logger.info(
        "Method=%s Path=%s StatusCode=%s ProcessTime=%s",
        request.method,
        request.url.path,
        response.status_code,
        process_time,
    )

    return response


app.include_router(budgets.router)
app.include_router(expenses.router)
