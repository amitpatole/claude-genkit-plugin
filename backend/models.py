from typing import Any, Dict

class ScheduleEnforcementRule:
    __slots__ = ["id", "non_dev_start", "non_dev_end"]

    def __init__(self, id: int, non_dev_start: time, non_dev_end: time):
        self.id = id
        self.non_dev_start = non_dev_start
        self.non_dev_end = non_dev_end