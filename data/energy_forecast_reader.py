import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta, timezone

from data.data_reader import DataReader

class EnergyForecastReader(DataReader):
    """
    A reader class for energy forecast data, either from a database or generated dummy data.
    
    Configuration Parameters:
        - P_max (int, float): Maximum solar production value (default: 100).
        - sigma (float): Controls the spread of the Gaussian curve for solar production (default: 3).
        - consumption (dict): Office consumption profiles, including ranges for different times of day.
            - night (tuple): Energy consumption during the night (default: (5, 10)).
            - morning (tuple): Energy consumption during the morning ramp-up (default: (20, 40)).
            - day (tuple): Energy consumption during the peak daytime hours (default: (50, 80)).
            - evening (tuple): Energy consumption during the evening decline (default: (20, 40)).
    
    Example:
        # Initialize with default parameters
        reader = EnergyForecastReader(db_connector=None)

        # Initialize with custom parameters
        custom_config = {
            'P_max': 120,
            'sigma': 4,
            'consumption': {
                'night': (10, 15),
                'morning': (25, 45),
                'day': (60, 100),
                'evening': (30, 50)
            }
        }
        reader = EnergyForecastReader(db_connector=None, config=custom_config)
    """
    
    DEFAULT_PARAMS = {
        'P_max': 100,  
        'sigma': 3,    
        'consumption': {
            'night': (5, 10),  
            'morning': (20, 40),  
            'day': (50, 80),  
            'evening': (20, 40)  
        }
    }
    
    def __init__(self, db_connector, config=None):
        """
        Initializes the EnergyForecastReader with optional custom configuration.
        
        Parameters:
            db_connector: The database connection object.
            config (dict, optional): Custom configuration for the solar and consumption profiles.
                If not provided, defaults are used.
        """
        super().__init__(db_connector)
        self.config = config or self.DEFAULT_PARAMS


    def _generate_dummy_data(self, start_dt_utc: datetime = None, end_dt_utc: datetime = None) -> pd.DataFrame:

        if not start_dt_utc:
            start_dt_utc = datetime.now(timezone.utc) - timedelta(days=7)
        if not end_dt_utc:
            end_dt_utc = datetime.now(timezone.utc)

        datetime_range = pd.date_range(start=start_dt_utc, end=end_dt_utc, freq='15min')
        energy_kwh = [self._solar_production(dt) - self._office_consumption(dt) for dt in datetime_range]

        return pd.DataFrame({'datetime': datetime_range, 'energy_kwh': energy_kwh})

    def _solar_production(self, dt: datetime) -> float:
        """Calculates solar production based on Gaussian curve."""
        peak_hour = 12
        sigma = self.config['sigma']  
        if dt.hour < 6 or dt.hour > 18:  # No production at night
            return 0
        return self.config['P_max'] * np.exp(-((dt.hour - peak_hour) ** 2) / (2 * sigma ** 2))

    def _office_consumption(self, dt: datetime) -> float:
        """Calculates office consumption based on time of day."""
        consumption = self.config['consumption']
        if dt.hour < 6 or dt.hour > 20:
            return np.random.uniform(*consumption['night'])
        elif 6 <= dt.hour < 9:
            return np.random.uniform(*consumption['morning'])
        elif 9 <= dt.hour < 17:
            return np.random.uniform(*consumption['day'])
        elif 17 <= dt.hour <= 20:
            return np.random.uniform(*consumption['evening'])
