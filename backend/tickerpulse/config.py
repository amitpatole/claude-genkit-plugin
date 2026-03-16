class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///tickerpulse.db?mode=memory&cache=shared'
    SQLALCHEMY_TRACK_MODIFICATIONS = False