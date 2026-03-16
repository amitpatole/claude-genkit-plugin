from typing import Any, AsyncContextManager, AsyncGenerator, Optional
import logging
from sqlite3 import Row
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, MetaData, Table, select, Column, String, Integer

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

DATABASE_URL = "sqlite+aiosqlite:///./genkit_plugin.db"

engine = create_async_engine(DATABASE_URL, connect_args={"check_same_thread": False}, echo=True)
async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

metadata = MetaData()

snippets = Table(
    "snippets",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("snippet", String),
    Column("context", String),
)

applied_snippets = Table(
    "applied_snippets",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("snippet", String),
    Column("context", String),
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Get an async database session.
    :return: An async generator yielding an AsyncSession.
    """
    async with asynccontextmanager(async_session) as session:
        yield session