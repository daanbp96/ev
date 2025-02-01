import os
from datetime import timedelta 

from logic.dispatcher import Dispatcher
from data.energy_forecast_reader import EnergyForecastReader
from data.session_reader import SessionReader
from common.helper_functions import run_local

if run_local:
    database_connector = None
else:
    pass

session_handler = SessionReader(database_connector)
sessions = session_handler.read()

production_forecast = EnergyForecastReader(database_connector)


dispatcher = Dispatcher(sessions, production_forecast)

current_time = sessions["start_dt_utc"].min()
while current_time <= sessions["end_dt_utc"].max():
    if dispatcher.is_triggered(current_time):
        pass

    current_time += timedelta(seconds=5) 

print('klaar')

