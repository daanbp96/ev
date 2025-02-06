import pandas as pd
from datetime import datetime

class SmartMeter:
    def __init__(self,
                 meter_values: pd.DataFrame):
        self.meter_values = meter_values
    
    def get_meter_values(self,
                         start_dt_utc: datetime,
                         end_dt_utc: datetime):
        return self.meter_values[
                (self.meter_values["start_dt_utc"] >= start_dt_utc) 
                & (self.meter_values["end_dt_utc"] < end_dt_utc)
            ]
        