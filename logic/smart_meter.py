import pandas as pd
from datetime import datetime

class SmartMeter:
    def __init__(self,
                 meter_values: pd.DataFrame):
        self.meter_values = meter_values

    def get_meter_values(self, start_dt_utc: datetime,
                         end_dt_utc: datetime
                         ):
        
        meter_values = self.meter_values[
            (self.meter_values["start_dt_utc"] >= start_dt_utc) 
            & (self.meter_values["end_dt_utc"] <= end_dt_utc)
        ]
        if meter_values.empty:
            min_start_dt = self.meter_values["start_dt_utc"].min()
            max_end_dt = self.meter_values["end_dt_utc"].max()

            if end_dt_utc < min_start_dt:
                raise ValueError(f"Error: end_dt_utc ({end_dt_utc}) is before the earliest meter value start datetime ({min_start_dt}).")
            
            if start_dt_utc > max_end_dt:
                raise ValueError(f"Error: start_dt_utc ({start_dt_utc}) is after the latest meter value end datetime ({max_end_dt}).")

            raise ValueError("Error: No meter values found for the given time range, but the reason is unknown.")

        return meter_values


        