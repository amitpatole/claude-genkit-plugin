from flask import Flask
from backend.utils.db import get_db_connection

def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object('config.DevelopmentConfig')

    @app.before_first_request
    async def initialize_db() -> None:
        await get_db_connection()

    return app