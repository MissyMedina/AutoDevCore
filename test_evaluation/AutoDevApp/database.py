"""
Optimized Database Configuration with Connection Pooling
"""

import os
from contextlib import asynccontextmanager, contextmanager
from typing import AsyncGenerator, Generator

from sqlalchemy import create_engine, event
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool, StaticPool

# Database URL - use environment variable or default to SQLite
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")
ASYNC_DATABASE_URL = os.getenv("ASYNC_DATABASE_URL", "sqlite+aiosqlite:///./app.db")

# Optimized engine configuration with connection pooling
engine_kwargs = {
    "echo": False,  # Set to True for SQL debugging
    "future": True,
}

if DATABASE_URL.startswith("sqlite"):
    # SQLite-specific optimizations
    engine_kwargs.update(
        {
            "connect_args": {
                "check_same_thread": False,
                "timeout": 20,
                "isolation_level": None,  # Autocommit mode
            },
            "poolclass": StaticPool,
            "pool_pre_ping": True,
        }
    )
else:
    # PostgreSQL/MySQL optimizations
    engine_kwargs.update(
        {
            "poolclass": QueuePool,
            "pool_size": 10,
            "max_overflow": 20,
            "pool_pre_ping": True,
            "pool_recycle": 3600,  # Recycle connections every hour
        }
    )

# Synchronous engine
engine = create_engine(DATABASE_URL, **engine_kwargs)

# Async engine for better performance
async_engine = create_async_engine(ASYNC_DATABASE_URL, **engine_kwargs)

# Session makers
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
AsyncSessionLocal = async_sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)


# SQLite performance optimizations
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    """Set SQLite pragmas for better performance."""
    if "sqlite" in str(dbapi_connection):
        cursor = dbapi_connection.cursor()
        # Enable WAL mode for better concurrency
        cursor.execute("PRAGMA journal_mode=WAL")
        # Increase cache size (negative value = KB)
        cursor.execute("PRAGMA cache_size=-64000")  # 64MB cache
        # Enable foreign key constraints
        cursor.execute("PRAGMA foreign_keys=ON")
        # Optimize synchronous mode
        cursor.execute("PRAGMA synchronous=NORMAL")
        # Set temp store to memory
        cursor.execute("PRAGMA temp_store=MEMORY")
        cursor.close()


@contextmanager
def get_db() -> Generator[SessionLocal, None, None]:
    """Get database session with proper cleanup."""
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


@asynccontextmanager
async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    """Get async database session with proper cleanup."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


# Legacy compatibility function
def get_db_legacy():
    """Legacy database session getter for backward compatibility."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
