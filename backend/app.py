from typing import Any
import logging
from flask import Flask
from backend.schedule_enforcement.schedule_enforcement import enforce_schedule

app = Flask(__name__)

@app.before_request
async def before_request() -> None:
    """Enforce schedule before each request."""
    user_id = "user123"  # Replace with actual user ID retrieval logic
    deployment_time = datetime.now(timezone.utc)
    await enforce_schedule(user_id, deployment_time)

if __name__ == "__main__":
    app.run()