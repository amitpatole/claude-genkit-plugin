from typing import Any
import logging
from datetime import datetime, timezone
from flask import current_app
from sqlite3 import Row
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select

from .models import ScheduleEnforcementRule, ScheduleEnforcementLog

logger = logging.getLogger(__name__)

# Define the database engine and sessionmaker
DATABASE_URL = current_app.config['DATABASE_URL']
engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)

@asynccontextmanager
async def get_async_session() -> AsyncSession:
    async with async_session() as session:
        yield session

async def enforce_schedule_rules() -> None:
    async with get_async_session() as session:
        now = datetime.now(timezone.utc)
        query = select(ScheduleEnforcementRule).where(
            ScheduleEnforcementRule.start_time <= now,
            ScheduleEnforcementRule.end_time >= now
        )
        result = await session.execute(query)
        rules = result.scalars().all()

        for rule in rules:
            if rule.schedule_type == 'non_dev_hours':
                await log_non_dev_hours_enforcement(rule, session, now)

async def log_non_dev_hours_enforcement(rule: ScheduleEnforcementRule, session: AsyncSession, now: datetime) -> None:
    log_entry = ScheduleEnforcementLog(
        rule_id=rule.id,
        enforcement_time=now,
        message=f"Enforced rule {rule.id} during non-development hours"
    )
    session.add(log_entry)
    await session.commit()

# Ensure the database is in WAL mode
async def ensure_wal_mode() -> None:
    async with get_async_session() as session:
        await session.execute("PRAGMA journal_mode=WAL")
        await session.commit()

# Initialize the schedule enforcement agent
async def init_schedule_enforcement_agent() -> None:
    await ensure_wal_mode()
    await enforce_schedule_rules()