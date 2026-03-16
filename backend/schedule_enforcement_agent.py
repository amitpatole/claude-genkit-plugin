from typing import Any
import logging
from datetime import datetime, timezone
from flask import current_app
import sqlite3
from sqlite3 import Error

logging.basicConfig(level=logging.INFO)

def get_allowed_hours() -> tuple[datetime, datetime]:
    """Returns the start and end of allowed hours in EST timezone."""
    start_time = datetime(1, 1, 1, 22, 0, 0, tzinfo=timezone(-5, 'EST'))
    end_time = datetime(1, 1, 1, 8, 0, 0, tzinfo=timezone(-5, 'EST'))
    return start_time, end_time

def is_within_allowed_hours(current_time: datetime) -> bool:
    """Checks if the current time is within the allowed deployment hours."""
    allowed_start, allowed_end = get_allowed_hours()
    return allowed_start <= current_time <= allowed_end

def log_deployment_attempt(deployment_time: datetime, is_scheduled: bool) -> None:
    """Logs the deployment attempt with the given time and whether it was scheduled."""
    log_message = f"Deployment attempt at {deployment_time} {'scheduled' if is_scheduled else 'blocked'}"
    logging.info(log_message)

def notify_user(deployment_time: datetime, is_scheduled: bool) -> None:
    """Notifies the user via the Genkit Explorer sidebar about the deployment attempt."""
    message = f"Deployment at {deployment_time} {'scheduled' if is_scheduled else 'blocked'}"
    current_app.genkit_explorer.notify(message)

def block_deployment(deployment_time: datetime) -> None:
    """Blocks the deployment if it's outside the allowed hours and logs the violation."""
    if not is_within_allowed_hours(deployment_time):
        log_deployment_attempt(deployment_time, is_scheduled=False)
        notify_user(deployment_time, is_scheduled=False)

def log_deployment_result(deployment_time: datetime, is_scheduled: bool) -> None:
    """Logs the result of the deployment attempt."""
    log_deployment_attempt(deployment_time, is_scheduled)
    if not is_scheduled:
        notify_user(deployment_time, is_scheduled=False)

def handle_deployment(deployment_time: datetime) -> None:
    """Handles the deployment attempt, blocking it if necessary."""
    block_deployment(deployment_time)
    log_deployment_result(deployment_time, is_scheduled=False)

def main() -> None:
    """Main function to simulate deployment attempts and handle them."""
    deployment_times = [
        datetime(2023, 10, 10, 23, 59, 59, tzinfo=timezone(-5, 'EST')),  # Scheduled
        datetime(2023, 10, 10, 9, 0, 0, tzinfo=timezone(-5, 'EST')),     # Blocked
        datetime(2023, 10, 10, 22, 0, 0, tzinfo=timezone(-5, 'EST')),   # Scheduled
        datetime(2023, 10, 10, 7, 59, 59, tzinfo=timezone(-5, 'EST')),  # Blocked
    ]

    for deployment_time in deployment_times:
        handle_deployment(deployment_time)

if __name__ == "__main__":
    main()