from dotenv import load_dotenv

# Load environment variables
load_dotenv(".env", verbose = True)

import os
from datetime import timedelta

from logic.dispatcher import Dispatcher
from logic.optimizer import Optimizer
from logic.trigger_checker import TriggerChecker
from logic.charging_hub import ChargingHub
from logic.charging_logger import ChargingLogger

from logic.smart_meter import SmartMeter
from data.energy_forecast_reader import EnergyForecastReader
from data.session_reader import SessionReader
from data.meter_value_reader import MeterValueReader
from common.helper_functions import run_local

TIME_STEP = timedelta(minutes=15)

RUN_LOCAL = os.getenv("RUN_LOCAL", "False").strip().lower() == "true"

if RUN_LOCAL:
    database_connector = None
else:
    # Get DB connector specified for platform (implement later)
    database_connector = "DB_CONNECTION_PLACEHOLDER"

session_reader = SessionReader(database_connector)
sessions = session_reader.read()
energy_forecast_reader = EnergyForecastReader(database_connector)
energy_forecast = energy_forecast_reader.read()

meter_value_reader = MeterValueReader(database_connector)
meter_values = meter_value_reader.read(energy_forecast=energy_forecast)

charging_logger = ChargingLogger()
smart_meter = SmartMeter(meter_values)
trigger_checker = TriggerChecker(sessions)
charging_hub = ChargingHub(sessions, smart_meter)
optimizer = Optimizer()

dispatcher = Dispatcher(trigger_checker, charging_hub, optimizer, charging_logger)

start_time = sessions["start_dt_utc"].min().floor("15min")
end_time = sessions["end_dt_utc"].max().floor("15min")

dispatcher.run(start_time, end_time, TIME_STEP)

print('klaar')

