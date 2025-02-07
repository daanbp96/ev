from datetime import datetime, timedelta
from logic.optimizer import Optimizer
from logic.trigger_checker import TriggerChecker
from logic.charging_hub import ChargingHub
from logic.charging_logger import ChargingLogger
import pandas as pd

class Dispatcher:
    def __init__(self,
                 trigger_checker: TriggerChecker,
                 charging_hub: ChargingHub,
                 optimizer: Optimizer,
                 charging_logger: ChargingLogger
                 ):
        self.trigger_checker = trigger_checker
        self.optimizer = optimizer
        self.charging_hub = charging_hub
        self.charging_logger = charging_logger

    def run(self,
            start_dt_utc: datetime,
            end_dt_utc: datetime,
            timestep: timedelta) -> bool:
        
        result = pd.DataFrame()
        current_dt_utc = start_dt_utc
        signals = pd.DataFrame()

        while current_dt_utc <= end_dt_utc:
            if self.trigger_checker.is_triggered(current_dt_utc, result, signals):
                charging_cars = self.charging_hub.get_charging_cars(current_dt_utc)
                if not charging_cars.empty:
                    signals = self.optimizer.optimize_sessions(current_dt_utc, charging_cars)
                    result = self.charging_hub.charge(signals, current_dt_utc, timestep)                    
            self.charging_logger.log(current_dt_utc, result)
            current_dt_utc += timestep        
        self.charging_logger.flush_to_dataframe()

            

