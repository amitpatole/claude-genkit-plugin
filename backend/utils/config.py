from typing import Any

def get_config() -> dict[str, Any]:
    return {
        "allowed_hours": [(22, 8)],
        "log_file_path": "logs/schedule_violations.log",
        "db": {
            "path": "tickerpulse.db"
        }
    }