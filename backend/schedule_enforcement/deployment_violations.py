from typing import List
from datetime import datetime
from sqlite3 import Row

class DeploymentViolation:
    @staticmethod
    def get_all_violations() -> List[Row]:
        with sqlite3.connect("tickerpulse.db", uri=True, isolation_level=None, detect_types=sqlite3.PARSE_DECLTYPES) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM deployment_violations")
            return cursor.fetchall()