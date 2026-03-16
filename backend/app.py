from typing import Any
from flask import Flask, current_app
from .schedule_enforcement import enforce_schedule

app = Flask(__name__)

@app.before_request
async def before_request():
    user_id = current_app.config.get("CURRENT_USER_ID")
    deployment_time = datetime.now(timezone.utc).astimezone(timezone(offset=-(5, 0)))  # EST is UTC-5
    await enforce_schedule(user_id, deployment_time)