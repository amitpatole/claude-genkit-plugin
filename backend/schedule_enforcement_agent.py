from typing import Any, Dict, Optional
import sqlite3
from sqlite3 import Row
from datetime import datetime, time
from flask import current_app

from config import SCHEDULE_ENFORCEMENT_DB_PATH

logging.basicConfig(level=logging.INFO)

def get_current_time() -> time:
    return datetime.now().time()

def is_non_dev_hour(current_time: time) -> bool:
    non_dev_hours_start = time(hour=18, minute=0, second=0)
    non_dev_hours_end = time(hour=8, minute=0, second=0)
    return non_dev_hours_start <= current_time < non_dev_hours_end

def get_non_dev_hours_schedule() -> Dict[str, time]:
    conn = sqlite3.connect(SCHEDULE_ENFORCEMENT_DB_PATH, uri=True, uri_same_file=True, detect_types=sqlite3.PARSE_DECLTYPES, isolation_level=None, row_factory=Row)
    cursor = conn.cursor()
    cursor.execute("SELECT task_name, start_time, end_time FROM schedule WHERE is_non_dev_hour = 1")
    schedule = {row['task_name']: time(row['start_time'].hour, row['start_time'].minute, row['start_time'].second) for row in cursor.fetchall()}
    conn.close()
    return schedule

async def enforce_schedule() -> None:
    current_time = get_current_time()
    if is_non_dev_hour(current_time):
        non_dev_schedule = await get_non_dev_hours_schedule()
        for task_name, task_time in non_dev_schedule.items():
            logging.info(f"Task {task_name} is scheduled for {task_time} during non-dev hours.")
    else:
        logging.info("Not in non-dev hours, no schedule enforcement needed.")