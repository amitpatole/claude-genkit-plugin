import os

def get_config() -> dict:
    return {
        'database_url': os.environ.get('DB_URL', 'sqlite+aiosqlite:///./test.db'),
        'debug': os.environ.get('DEBUG', 'False').lower() == 'true',
    }