from contextlib import asynccontextmanager

from fastapi import FastAPI

from . import models
from .api.routes import router
from .core.config import PROJECT_NAME
from .database.connection import SessionLocal, test_connection
from .services.memory_cleanup_service import (
    memory_cleanup_service,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Test database connection
    test_connection()

    # Run memory cleanup on startup
    db = SessionLocal()

    try:
        result = memory_cleanup_service.cleanup(db)

        print(
            f"[Memory Cleanup] "
            f"Processed={result['processed']} | "
            f"Archived={result['archived']} | "
            f"Forgotten={result['forgotten']}"
        )

    finally:
        db.close()

    yield


app = FastAPI(
    title=PROJECT_NAME,
    description="Backend API for the AI Personal Memory & Decision Assistant.",
    version="1.0.0",
    contact={
        "name": "Anushka",
        "email": "aanushka0386@gmail.com",
    },
    lifespan=lifespan,
)

app.include_router(router)