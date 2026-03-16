from typing import Any
import logging
from sqlite3 import Error, Row
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, text

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URI')
db = SQLAlchemy(app)

def init_db() -> None:
    """Initialize the database with the necessary tables."""
    with app.app_context():
        db.create_all()

def get_db_connection() -> Row:
    """Return a connection to the SQLite database."""
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], isolation_level='SERIALIZABLE', journal_mode='WAL')
    conn = engine.connect()
    conn.row_factory = Row
    return conn

def add_dependency(name: str, version: str) -> None:
    """Add a new dependency to the database."""
    try:
        with get_db_connection() as conn:
            conn.execute(text("INSERT INTO dependencies (name, version) VALUES (:name, :version)"), {"name": name, "version": version})
            conn.commit()
    except Error as e:
        logging.error(f"Database error: {e}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

def update_dependency(name: str, version: str) -> None:
    """Update an existing dependency in the database."""
    try:
        with get_db_connection() as conn:
            conn.execute(text("UPDATE dependencies SET version = :version WHERE name = :name"), {"name": name, "version": version})
            conn.commit()
    except Error as e:
        logging.error(f"Database error: {e}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

def get_dependencies() -> list[Row]:
    """Fetch all dependencies from the database."""
    try:
        with get_db_connection() as conn:
            result = conn.execute(text("SELECT * FROM dependencies")).fetchall()
            return result
    except Error as e:
        logging.error(f"Database error: {e}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
    return []