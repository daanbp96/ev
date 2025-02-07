import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta, timezone

from data.data_reader import DataReader

class EnergyForecastReader(DataReader):
    """
    A reader class for energy forecast data, either from a database or generated dummy data.
    
    Configuration Parameters:
        - P_max (float): Maximum solar production at peak (default: 100).
        - sigma (float): Controls the spread of the Gaussian curve for solar production (default: 3).
        - sunrise (int): Hour of the day when solar production starts (default: 6).
        - sunset (int): Hour of the day when solar production stops (default: 18).
        - peak_hour (int): Hour of the day when solar production is at its highest (default: 12).
        - consumption (dict): Office consumption profiles, including ranges for different times of day.
            - night (tuple): Energy consumption during the night (default: (5, 10)).
            - morning (tuple): Energy consumption during the morning ramp-up (default: (20, 40)).
            - day (tuple): Energy consumption during the peak daytime hours (default: (50, 80)).
            - evening (tuple): Energy consumption during the evening decline (default: (20, 40)).

    Example:
        # Initialize with default parameters
        reader = EnergyForecastReader(db_connector=db_connector)

        # Initialize with custom parameters
        custom_config = {
            'P_max': 120,
            'sigma': 4,
            'sunrise': 5,
            'sunset': 19,
            'peak_hour': 13,
            'consumption': {
                'night': (10, 15),
                'morning': (25, 45),
                'day': (60, 100),
                'evening': (30, 50)
            }
        }
        reader = EnergyForecastReader(db_connector=db_connector, config=custom_config)
    """

    DEFAULT_PARAMS = {
        'P_max': 100,  
        'sigma': 3,    
        'sunrise': 6,    # Default: 6 AM
        'sunset': 18,    # Default: 6 PM
        'peak_hour': 12, # Default: Solar noon at 12 PM
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

    def read(self, 
             path: str = None, 
             start_dt_utc: datetime = None, 
             end_dt_utc: datetime = None
             ) -> pd.DataFrame:
        """Reads the energy data, either from a database or generates dummy data."""
        if os.getenv("USE_DUMMY_DATA", "False").lower() == "true":
            energy_forecast = self._generate_dummy_data(start_dt_utc, end_dt_utc)
        else:
            energy_forecast = pd.DataFrame()

        if os.getenv("DEBUG_MODE", "False").lower() == "true":
            print("Energy forecast data:")
            print(f"Start datetime (UTC): {energy_forecast['start_dt_utc'].min()}")
            print(f"Last end datetime (UTC): {energy_forecast['end_dt_utc'].max()}")
            print(f"Total number of rows: {len(energy_forecast)}")  
        
        return energy_forecast

    def _generate_dummy_data(self, 
                             start_dt_utc: datetime = None, 
                             end_dt_utc: datetime = None
                             ) -> pd.DataFrame:
        """
        Generates dummy energy forecast data in 15-minute intervals.

        Parameters:
            start_dt_utc (datetime, optional): Start datetime in UTC.
            end_dt_utc (datetime, optional): End datetime in UTC.

        Returns:
            pd.DataFrame: A DataFrame containing energy forecasts.
        """
        if not start_dt_utc:
            start_dt_utc = (datetime.now(timezone.utc) - timedelta(days=7)).replace(hour=0, minute=0, second=0, microsecond=0)
        if not end_dt_utc:
            end_dt_utc = datetime.now(timezone.utc)

        start_dt_utc = pd.Timestamp(start_dt_utc).floor("15min")
        end_dt_utc = pd.Timestamp(end_dt_utc).floor("15min")            

        start_dt_range = pd.date_range(start=start_dt_utc, end=end_dt_utc, freq='15min')
        end_dt_range = start_dt_range + timedelta(minutes=15)

        energy_kwh = [(self._solar_production(dt) - self._office_consumption(dt)) for dt in start_dt_range]

        return pd.DataFrame({'start_dt_utc': start_dt_range,
                              'end_dt_utc': end_dt_range,
                              'energy_kwh': energy_kwh})

    def _solar_production(self, dt: datetime) -> float:
        """
        Generates a smooth Gaussian-based solar production curve.

        The production follows a Gaussian curve peaking at `peak_hour`, with 
        zero production before `sunrise` and after `sunset`.

        Config Parameters:
            - P_max (float): Maximum solar production at peak.
            - sigma (float): Controls the spread of the Gaussian curve.
            - sunrise (int): Hour of the day when solar production starts.
            - sunset (int): Hour of the day when solar production stops.
            - peak_hour (int): Hour of the day when solar production is at its highest.

        Returns:
            float: Solar energy production in kWh.
        """
        P_max = self.config['P_max']
        sigma = self.config['sigma']
        sunrise = self.config['sunrise']
        sunset = self.config['sunset']
        peak_hour = self.config['peak_hour']

        # Convert to hour of day as a float
        hour = dt.hour + dt.minute / 60

        # No production before sunrise or after sunset
        if hour < sunrise or hour > sunset:
            return 0

        # Gaussian curve centered at peak_hour
        production = P_max * np.exp(-((hour - peak_hour) ** 2) / (2 * sigma ** 2))

        return max(0, production)  # Ensure no negative values

    def _office_consumption(self, dt: datetime) -> float:
        """
        Calculates office consumption based on time of day.

        Config Parameters:
            - consumption (dict): Contains different time-of-day consumption profiles.
                - night (tuple): Energy consumption during the night.
                - morning (tuple): Energy consumption during the morning ramp-up.
                - day (tuple): Energy consumption during the peak daytime hours.
                - evening (tuple): Energy consumption during the evening decline.

        Returns:
            float: Randomized energy consumption within the given time-of-day range.
        """
        consumption = self.config['consumption']
        if dt.hour < 6 or dt.hour > 20:
            return np.random.uniform(*consumption['night'])
        elif 6 <= dt.hour < 9:
            return np.random.uniform(*consumption['morning'])
        elif 9 <= dt.hour < 17:
            return np.random.uniform(*consumption['day'])
        elif 17 <= dt.hour <= 20:
            return np.random.uniform(*consumption['evening'])
