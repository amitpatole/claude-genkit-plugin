from typing import List
from datetime import datetime
from sqlite3 import Row

class DeploymentViolation:
    def __init__(self, deployment_time: datetime):
        self.deployment_time = deployment_time

    @staticmethod
    def get_violations() -> List[DeploymentViolation]:
        conn = sqlite3.connect(DB_PATH, isolation_level=None, detect_types=sqlite3.PARSE_DECLTYPES)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT deployment_time FROM deployment_violations")
            rows = cursor.fetchall()
            return [DeploymentViolation(datetime.strptime(row['deployment_time'], '%Y-%m-%d %H:%M:%S')) for row in rows]
        finally:
            cursor.close()
            conn.close()