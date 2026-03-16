from typing import Any, Dict
import os

def get_env_var(var_name: str, default: Any = None) -> Any:
    """Retrieve an environment variable or return a default value."""
    return os.getenv(var_name, default)