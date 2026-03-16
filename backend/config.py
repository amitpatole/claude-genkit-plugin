from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from backend.utils import get_env_var

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = get_env_var('DB_URI', 'sqlite:///monitoring.db?mode=memory&cache=shared')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)