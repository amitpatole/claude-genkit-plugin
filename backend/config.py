from os import environ

class Config:
    DATABASE_URL = environ.get('DATABASE_URL', 'sqlite:///tickerpulse.db')