# Configuration for TickerPulse
import os

class Config:
    DB_PATH = os.environ.get("DB_PATH", "tickerpulse.db")
    NON_DEV_HOURS = os.environ.get("NON_DEV_HOURS", {})

# Development configuration
class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(os.getcwd(), Config.DB_PATH)}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# Production configuration
class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(os.getcwd(), Config.DB_PATH)}"

# Initialize app with development config
app = Flask(__name__)
app.config.from_object(DevelopmentConfig)