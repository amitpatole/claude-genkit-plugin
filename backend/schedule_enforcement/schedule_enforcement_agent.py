from datetime import datetime, timezone
from typing import Any
import logging
from flask import current_app

from config import SCHEDULE_ENFORCEMENT_CONFIG
from utils.db import get_db_connection
from utils.notifications import send_genkit_explorer_notification

logger = logging.getLogger(__name__)

def is_allowed_time() -> bool:
    """
    Check if the current time is within the allowed deployment hours (10 PM - 8 AM EST).

    :return: True if within allowed hours, False otherwise.
    """
    now = datetime.now(timezone('EST'))
    return 22 <= now.hour < 24 or 0 <= now.hour < 8

def log_violation(deployment_id: int, reason: str) -> None:
    """
    Log a deployment violation to a file.

    :param deployment_id: ID of the deployment attempt.
    :param reason: Reason for the violation.
    """
    with open("violation_logs.txt", "a") as log_file:
        log_file.write(f"VIOLATION: Deployment {deployment_id} attempted at {datetime.now().isoformat()} - {reason}\n")

def notify_user(deployment_id: int, reason: str) -> None:
    """
    Notify the user via the Genkit Explorer sidebar of a deployment violation.

    :param deployment_id: ID of the deployment attempt.
    :param reason: Reason for the violation.
    """
    send_genkit_explorer_notification(
        title="Deployment Violation",
        message=f"Deployment {deployment_id} attempted outside allowed hours - {reason}",
        level="warning"
    )

def enforce_schedule(deployment_id: int) -> None:
    """
    Enforce schedule by blocking deployments outside the allowed hours and logging violations.

    :param deployment_id: ID of the deployment attempt.
    """
    if not is_allowed_time():
        reason = "Deployment attempted outside allowed hours (10 PM - 8 AM EST)"
        log_violation(deployment_id, reason)
        notify_user(deployment_id, reason)

def main() -> None:
    """
    Main entry point for the Schedule Enforcement Agent.
    """
    deployment_id = 12345  # Example deployment ID
    enforce_schedule(deployment_id)

if __name__ == "__main__":
    main()