import os
from contextlib import contextmanager
from pathlib import Path
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from config.settings import settings
from src.storage.models import Base
from src.utils.logging import app_logger

# Ensure parent directory for SQLite exists
if settings.DATABASE_URL.startswith("sqlite"):
    db_path = settings.DATABASE_URL.replace("sqlite:///", "")
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)

engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {},
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db() -> None:
    """Creates database tables if they do not already exist."""
    app_logger.info(f"Initializing database schema at {settings.DATABASE_URL}")
    Base.metadata.create_all(bind=engine)
    app_logger.info("Database tables verified/created successfully.")

@contextmanager
def get_db_session() -> Generator[Session, None, None]:
    """Context manager for transaction management."""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        app_logger.error(f"Database session rolled back due to error: {e}")
        raise e
    finally:
        session.close()

def get_db() -> Generator[Session, None, None]:
    """Dependency generator for FastAPI endpoints."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
