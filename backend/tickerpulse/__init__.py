from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_socketio import SocketIO
from flask_talisman import Talisman
from flask_talisman import Talisman
from .schedule_enforcement_agent import ScheduleEnforcementAgent

app = Flask(__name__)
app.config.from_object("config.DevelopmentConfig")
db = SQLAlchemy(app)
migrate = Migrate(app, db)
cache = Cache(app)
limiter = Limiter(app, key_func=get_remote_address)
cors = CORS(app)
jwt = JWTManager(app)
mail = Mail(app)
socketio = SocketIO(app)
talisman = Talisman(app)
schedule_enforcement_agent = ScheduleEnforcementAgent(db_path=app.config["DB_PATH"])

# Initialize extensions and blueprints
from . import auth, api, web  # Import blueprints here