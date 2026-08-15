import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


# Load .env from the main folder
BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = BASE_DIR / "main" / ".env"

load_dotenv(ENV_FILE)


# Get PostgreSQL database URL
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in main/.env")


# Create database engine
engine = create_engine(
    DATABASE_URL,
    echo=True
)


# Create database session
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# Base class for SQLAlchemy models
Base = declarative_base()


# Database dependency
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()