import pandas as pd
from datetime import datetime

class TriggerChecker:
    def __init__(self,
                 sessions: pd.DataFrame
                 ):
        self.sessions = sessions
    
    def is_triggered(self,
                     current_dt_utc: datetime,
                     result: pd.DataFrame,
                     signals: pd.DataFrame):
        if (self.sessions['start_dt_utc'] == current_dt_utc):
            return True
        if (self.sessions['end_dt_utc'] == current_dt_utc):
            return True
        if (result['charged_energy_kwh'] == 0):
            return True
        if (signals['end_dt_utc'] == current_dt_utc):
            return True
        else:
            return False

    def update_signals(self,
                       signals: pd.DataFrame):
        pass
