from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from ..core.config import DATABASE_URL

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def test_connection():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT version();"))
        print(result.scalar())