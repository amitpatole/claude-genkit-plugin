from typing import Any
import logging
from flask import current_app

def send_genkit_explorer_notification(title: str, message: str, level: str) -> None:
    """
    Send a notification to the Genkit Explorer sidebar.

    :param title: Title of the notification.
    :param message: Message content.
    :param level: Notification level (e.g., "info", "warning", "error").
    """
    logger.info(f"Sending notification: {title} - {message}")
    # Placeholder for actual notification sending logic
    pass