from typing import Any
import logging
from datetime import datetime, timezone
from flask import current_app
from sqlite3 import Row
from contextlib import asynccontextmanager
from backend.utils.config import get_config
from backend.utils.db import get_db_connection

logging.basicConfig(level=logging.INFO)

class ScheduleEnforcementAgent:
    def __init__(self):
        self.config = get_config()
        self.allowed_hours = self.config.get("allowed_hours", [])
        self.log_file_path = self.config.get("log_file_path", "logs/schedule_violations.log")

    async def check_allowed_hours(self, deployment_time: datetime) -> bool:
        current_hour = deployment_time.hour
        if self.allowed_hours:
            for allowed_hour in self.allowed_hours:
                if allowed_hour[0] <= current_hour < allowed_hour[1]:
                    return True
        return False

    async def log_violation(self, deployment_time: datetime, user_id: str, deployment_id: str) -> None:
        async with get_db_connection() as conn:
            conn.row_factory = Row
            cursor = conn.cursor()
            await cursor.execute(
                "INSERT INTO schedule_violations (deployment_time, user_id, deployment_id) VALUES (?, ?, ?)",
                (deployment_time, user_id, deployment_id)
            )
            await conn.commit()

    async def notify_user(self, deployment_time: datetime, user_id: str, deployment_id: str) -> None:
        # Simulate notification via Genkit Explorer sidebar
        logging.info(f"Deployment attempt at {deployment_time} is blocked. User ID: {user_id}, Deployment ID: {deployment_time}")

    async def enforce_schedule(self, deployment_time: datetime, user_id: str, deployment_id: str) -> None:
        if not await self.check_allowed_hours(deployment_time):
            await self.log_violation(deployment_time, user_id, deployment_id)
            await self.notify_user(deployment_time, user_id, deployment_id)

# Example usage
async def main():
    agent = ScheduleEnforcementAgent()
    deployment_time = datetime.now(timezone.utc)
    user_id = "user123"
    deployment_id = "deploy456"
    await agent.enforce_schedule(deployment_time, user_id, deployment_id)

# Run the example usage
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())