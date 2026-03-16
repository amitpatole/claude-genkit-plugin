from typing import Any
import asyncio

async def get_current_time() -> datetime:
    return datetime.now()