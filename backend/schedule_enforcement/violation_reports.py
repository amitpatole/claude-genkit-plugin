from typing import List
from datetime import datetime
from .schedule_enforcement_agent import enforce_schedule_with_db

class ViolationReports:
    def __init__(self, db_path: str, violation_log_path: str, genkit_explorer):
        self.db_path = db_path
        self.violation_log_path = violation_log_path
        self.genkit_explorer = genkit_explorer

    def enforce_schedule(self, deployment_id: int) -> None:
        enforce_schedule_with_db(deployment_id)

    def get_violation_reports(self) -> List[dict]:
        return [dict(report) for report in self.get_violation_reports_from_db()]

    def get_violation_reports_from_db(self) -> List[sqlite3.Row]:
        conn = sqlite3.connect(self.db_path, factory=sqlite3.Row)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT deployment_id, timestamp FROM violation_reports")
        return cursor.fetchall()

    def log_violation_to_db(self, deployment_id: int, timestamp: datetime) -> None:
        conn = sqlite3.connect(self.db_path, factory=sqlite3.Row)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("INSERT INTO violation_reports (deployment_id, timestamp) VALUES (?, ?)",
                       (deployment_id, timestamp))
        conn.commit()