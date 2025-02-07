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

    def _generate_dummy_data(self,
                             energy_forecast: datetime,
                             ) -> pd.DataFrame:
        """Generate meter values as deviations of forecast data."""
        
        energy_forecast['energy_kwh'] = energy_forecast['energy_kwh'].apply(self._apply_deviations)
        return energy_forecast

    def _apply_deviations(self, energy_kwh: float) -> float:
        """Apply random deviations to simulate real-world energy readings."""
        
        noise = np.random.normal(0, 5) 
        deviation = energy_kwh + noise
        
        if np.random.random() < 0.1: 
            spike = np.random.uniform(20, 50) 
            deviation += spike
        
        return max(deviation, 0)
