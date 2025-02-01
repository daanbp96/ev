from datetime import datetime
import pandas as pd

class Dispatcher:
    def __init__(self,
                 sessions: pd.DataFrame,
                 energy_forecast: pd.DataFrame
                 ):
        self.sessions = sessions
        self.energy_forecast = energy_forecast

    def is_triggered(self,
                     current_time: datetime) -> bool:
        return False
