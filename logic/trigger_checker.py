import pandas as pd

class TriggerChecker:
    def __init__(self,
                 sessions: pd.DataFrame,
                 energy_forecast: pd.DataFrame):
        self.sessions = sessions
        self.energy_forecast = energy_forecast
    
    def is_triggered(current_time):
        pass
