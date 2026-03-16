from typing import Any
import sqlite3
from sqlite3 import Row
from datetime import datetime, time
from flask import current_app
from backend.utils.db import get_db_connection

logging.basicConfig(level=logging.INFO)

def get_non_dev_hours() -> list[time]:
    return [
        time(hour=23, minute=00),
        time(hour=00, minute=00),
        time(hour=01, minute=00),
        time(hour=02, minute=00),
        time(hour=03, minute=00),
        time(hour=04, minute=00),
        time(hour=05, minute=00),
        time(hour=06, minute=00),
        time(hour=07, minute=00),
        time(hour=08, minute=00),
        time(hour=22, minute=00),
    ]

def is_within_non_dev_hours(current_time: time) -> bool:
    non_dev_hours = get_non_dev_hours()
    return any(hour <= current_time < (hour + time(1)) for hour in non_dev_hours)

async def enforce_schedule() -> None:
    conn = await get_db_connection()
    cursor = await conn.execute(
        "SELECT ticker, price FROM tickers WHERE last_update_time IS NULL OR last_update_time < datetime('now', '-1 hour')",
        (datetime.now().time(),)
    )
    rows = await cursor.fetchall()
    await cursor.close()
    await conn.close()

    for row in rows:
        ticker, price = row
        logging.info(f"Enforcing schedule for {ticker} with price {price}")

        # Simulate update logic here
        # await update_ticker(ticker, price)

async def main() -> None:
    current_time = datetime.now().time()
    if is_within_non_dev_hours(current_time):
        await enforce_schedule()