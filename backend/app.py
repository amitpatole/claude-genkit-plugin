from typing import Any
import sqlite3
import logging
from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from schedule_enforcement import enforce_schedule

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')

db = SQLAlchemy(app)
migrate = Migrate(app, db)

@app.before_request
async def before_request():
    g.db = db.session

@app.teardown_request
async def teardown_request(exception):
    db_session = getattr(g, 'db', None)
    if db_session:
        db_session.remove()

@app.before_first_request
async def before_first_request():
    await enforce_schedule()