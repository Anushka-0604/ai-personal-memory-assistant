from contextlib import asynccontextmanager

from fastapi import FastAPI

from .api.routes import router
from .core.config import PROJECT_NAME
from .database.connection import test_connection


@asynccontextmanager
async def lifespan(app: FastAPI):
    test_connection()
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