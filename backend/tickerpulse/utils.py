from typing import Any
import os
import logging

logger = logging.getLogger(__name__)

def get_db_path(db_name: str) -> str:
    return os.path.join(current_app.root_path, "db", db_name)