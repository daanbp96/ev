from dotenv import load_dotenv

# Load environment variables
load_dotenv(".env", verbose = True)

import os
import sys
from datetime import timedelta

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
#for notebook use:
#sys.path.append(os.path.abspath(".."))

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
import matplotlib.pyplot as plt


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


start_time = sessions["start_dt_utc"].min().floor("15min")
end_time = sessions["end_dt_utc"].max().floor("15min")



# Select a 2-day period from the start_time
plot_start = start_time
plot_end = start_time + timedelta(days=2)

# Filter data for the selected 2-day period
meter_values_filtered = meter_values[
    (meter_values["start_dt_utc"] >= plot_start) & 
    (meter_values["start_dt_utc"] < plot_end)
]

energy_forecast_filtered = energy_forecast[
    (energy_forecast["start_dt_utc"] >= plot_start) & 
    (energy_forecast["start_dt_utc"] < plot_end)
]

# Create the plot
plt.figure(figsize=(12, 6))  # Large figure size

# Plot meter values
plt.plot(meter_values_filtered["start_dt_utc"], meter_values_filtered["energy_kwh"], 
         label="Meter Values (kWh)", color="blue", linestyle="-")

# Plot energy forecast
plt.plot(energy_forecast_filtered["start_dt_utc"], energy_forecast_filtered["energy_kwh"], 
         label="Energy Forecast (kWh)", color="red", linestyle="--")

# Labels and title
plt.xlabel("Time (UTC)")
plt.ylabel("Energy (kWh)")
plt.title("Meter Values vs Energy Forecast (2-Day Period)")
plt.legend()
plt.grid(True)

# Show the plot
plt.show()