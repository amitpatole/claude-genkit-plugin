from schedule_enforcement_agent import enforce_schedule

# Ensure the schedule enforcement agent runs on startup
def on_startup() -> None:
    enforce_schedule()