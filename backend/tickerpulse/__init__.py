from flask import Flask
import os
from backend.tickerpulse.enforcement_agent import enforce_schedule

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')

@app.before_first_request
async def startup():
    logger = logging.getLogger(__name__)
    logger.info("Starting TickerPulse AI with schedule enforcement agent.")
    await enforce_schedule()