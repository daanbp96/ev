import pandas as pd
from datetime import datetime, timedelta
from logic.smart_meter import SmartMeter

class ChargingHub:
    def __init__(self,
                 sessions: pd.DataFrame,
                 smart_meter: SmartMeter,
                 max_gridpower_kw: int = 100):
        self.sessions = sessions
        self.smart_meter = smart_meter
        self.max_gridpower_kw = max_gridpower_kw

    def charge(self,
               signals: pd.DataFrame,
               current_dt_utc: datetime,
               timestep: timedelta):
        meter_value = self.smart_meter.get_meter_values(current_dt_utc, current_dt_utc + timestep)


        
        #check how much solar is available
        #check how much in total is available
        #check how much is asked
        #verdeel

        return pd.DataFrame()

    def get_charging_cars(self,
                           current_time: datetime)-> pd.DataFrame:
        
        return  self.sessions[
                (self.sessions["start_dt_utc"] >= current_time) 
                & (self.sessions["end_dt_utc"] < current_time)
                & (self.sessions['charged_energy_kwh'] < self.sessions['target_energy_kwh'])
            ]
        