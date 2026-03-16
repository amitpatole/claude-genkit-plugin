from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from backend.tickerpulse.schedule_enforcement_agent import enforce_schedule

app = Flask(__name__)
app.config.from_object('config.Config')

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Initialize the schedule enforcement agent
@app.before_first_request
async def init_schedule_enforcement():
    enforce_schedule()