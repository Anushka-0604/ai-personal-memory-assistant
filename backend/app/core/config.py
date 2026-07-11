from dotenv import load_dotenv
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent.parent

load_dotenv(BASE_DIR / ".env")

PROJECT_NAME = "AI Personal Memory & Decision Assistant API"

DATABASE_URL = os.getenv("DATABASE_URL")