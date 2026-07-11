from fastapi import FastAPI
from .core.config import PROJECT_NAME
from .api.routes import router
from .database.connection import test_connection
app = FastAPI(
    title=PROJECT_NAME,
    description="Backend API for the AI Personal Memory & Decision Assistant.",
    version="1.0.0",
    contact={
        "name": "Anushka",
        "email": "aanushka0386@gmail.com"
    }
)
app.include_router(router)
test_connection()