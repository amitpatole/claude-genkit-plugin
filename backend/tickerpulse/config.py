from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from contextlib import contextmanager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///genkit.db'
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

@contextmanager
def get_db_connection() -> sqlite3.Connection:
    conn = db.session.connection().engine.raw_connection()
    try:
        yield conn
    finally:
        conn.close()