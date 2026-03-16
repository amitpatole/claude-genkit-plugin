from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from backend.tickerpulse.schedule_enforcement_agent import main

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')
CORS(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Initialize the schedule enforcement agent
main()