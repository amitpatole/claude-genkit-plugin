from typing import Any
from datetime import datetime

class User:
    """
    Represents a user.
    """
    
    @classmethod
    def get_by_id(cls, user_id: int) -> Optional['User']:
        """
        Retrieves a user by ID.
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        if row:
            return cls(**row)
        return None