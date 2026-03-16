from typing import Any
import logging
from datetime import datetime, timedelta
from flask import current_app
from sqlite3 import Row
from contextlib import asynccontextmanager
from backend.database.db_manager import DBManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def db_session():
    db = DBManager(current_app.config['DATABASE'])
    try:
        await db.connect()
        yield db
    finally:
        await db.disconnect()

class ScheduleEnforcementAgent:
    def __init__(self, app):
        self.app = app
        self.allowed_start_time = datetime.strptime('22:00', '%H:%M').time()
        self.allowed_end_time = datetime.strptime('08:00', '%H:%M').time()

    async def is_allowed_time(self, current_time: datetime) -> bool:
        now = current_time.time()
        return self.allowed_start_time <= now < self.allowed_end_time or now < self.allowed_start_time

    async def enforce_schedule(self, deployment_time: datetime) -> bool:
        if not await self.is_allowed_time(deployment_time):
            logger.warning(f"Deployment attempt at {deployment_time} is outside allowed hours.")
            await self.log_violation(deployment_time)
            await self.notify_user(deployment_time)
            return False
        return True

    async def log_violation(self, deployment_time: datetime) -> None:
        async with db_session() as db:
            await db.execute(
                "INSERT INTO deployment_violations (time) VALUES (?)",
                (deployment_time,)
            )

    async def notify_user(self, deployment_time: datetime) -> None:
        # Notify user via Genkit Explorer sidebar
        pass  # Placeholder for actual implementation

    async def handle_deployment(self, deployment_time: datetime) -> bool:
        return await self.enforce_schedule(deployment_time)