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
            start_time: datetime,
            end_time: datetime,
            timestep: timedelta) -> bool:
        
        result = pd.DataFrame()
        current_time = start_time
        signals = None

        while current_time <= end_time:
            if signals is None or self.trigger_checker.is_triggered(current_time, result, signals):
                cars_charging = self.charging_hub.get_charging_cars(current_time)
                signals = self.optimizer.optimize_sessions(current_time, cars_charging)
            result = self.charging_hub.charge(signals)
            self.charging_logger.log(current_time, result)
            current_time += timestep        
        self.charging_logger.flush_to_dataframe()

            

