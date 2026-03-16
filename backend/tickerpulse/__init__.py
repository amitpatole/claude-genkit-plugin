from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .schedule_enforcement_agent import init_schedule_enforcement_agent

app = Flask(__name__)
app.config.from_object('config.Config')

db = SQLAlchemy(app)

@app.before_first_request
async def setup_db() -> None:
    await init_schedule_enforcement_agent()