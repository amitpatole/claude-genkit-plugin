from typing import Any
from flask import Flask

from backend.utils.db import get_db_connection

app = Flask(__name__)

# Initialize database connection
app.before_first_request(get_db_connection)