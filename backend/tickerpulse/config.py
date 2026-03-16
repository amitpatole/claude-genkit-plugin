class Config:
    DATABASE_PATH = os.environ['DATABASE_PATH']

class DevelopmentConfig(Config):
    pass