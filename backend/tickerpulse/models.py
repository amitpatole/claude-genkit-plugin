from typing import Any, Dict

class ScheduleEnforcementModel:
    def __init__(self, **kwargs: Dict[str, Any]):
        self.start_time = kwargs.get("start_time")
        self.end_time = kwargs.get("end_time")
        self.is_active = kwargs.get("is_active")