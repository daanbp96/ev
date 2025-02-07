import numpy as np
import pandas as pd
import os
from datetime import datetime, timedelta, timezone
from data.data_reader import DataReader
from data.energy_forecast_reader import EnergyForecastReader

class MeterValueReader(DataReader):
    def __init__(self, db_connector: object):
        super().__init__(db_connector)

    def read(self, 
             path: str = None,
             energy_forecast: pd.DataFrame = None, 
             start_dt_utc: datetime = None, 
             end_dt_utc: datetime = None
             ) -> pd.DataFrame:
        """Reads the energy data, either from a database or generates dummy data."""
        if os.getenv("USE_DUMMY_DATA", "False").lower() == "true":
            meter_values = self._generate_dummy_data(energy_forecast)
        else:
            meter_values = pd.DataFrame()
        if os.getenv("DEBUG_MODE", "False").lower() == "true":
            print("Metervalue data:")
            print(f"Start datetime (UTC): {meter_values['start_dt_utc'].min()}")
            print(f"Last end datetime (UTC): {meter_values['end_dt_utc'].max()}")
            print(f"Total number of rows: {len(meter_values)}")  
        return meter_values

    def _generate_dummy_data(self, energy_forecast: pd.DataFrame) -> pd.DataFrame:
        """Generate meter values as deviations of forecast data."""
        
        meter_values = energy_forecast.copy()
        
        # Apply deviations while passing the timestamp
        meter_values['energy_kwh'] = meter_values.apply(
            lambda row: self._apply_deviations(row['energy_kwh'], row['start_dt_utc']), axis=1
        )

        return meter_values

    def _apply_deviations(self, energy_kwh: float, timestamp: datetime) -> float:
        """Apply frequent small white noise variations and occasional spikes during the day."""
        deviation = energy_kwh
        if np.random.random() < 0.8:
            noise = np.random.uniform(-2, 2)
            deviation += noise    

        # Apply spikes only between 06:00 and 18:00
        if 6 <= timestamp.hour <= 18 and np.random.random() < 0.3:
            spike = np.random.uniform(-15, 15)
            deviation += spike

        return deviation


