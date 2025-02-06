import pandas as pd
from datetime import datetime

class ChargingHub:
    def __init__(self,
                 sessions: pd.DataFrame,
                 meter_values: pd.DataFrame):
        self.sessions = sessions
        self.meter_values = meter_values

    def charge(self,
               signals: pd.DataFrame):
        #charge
        pass

    def get_charging_cars(self,
                           current_time: datetime)-> pd.DataFrame:
        
        return  self.meter_values[
                (self.meter_values["start_dt_utc"] >= current_time) 
                & (self.meter_values["end_dt_utc"] < current_time)
            ]
        