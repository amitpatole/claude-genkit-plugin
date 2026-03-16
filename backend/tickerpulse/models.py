from typing import Any, Dict
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class ScheduleEnforcementLog(db.Model):
    __tablename__ = 'schedule_enforcement_logs'

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"ScheduleEnforcementLog(id={self.id}, timestamp={self.timestamp})"