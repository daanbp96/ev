from datetime import datetime, timedelta
from logic.optimizer import Optimizer
from logic.trigger_checker import TriggerChecker
from logic.charging_hub import ChargingHub
import pandas as pd

class Dispatcher:
    def __init__(self,
                 trigger_checker: TriggerChecker,
                 charging_hub: ChargingHub,
                 optimizer: Optimizer,
                 ):
        self.trigger_checker = trigger_checker
        self.optimizer = optimizer
        self.charging_hub = charging_hub

    def run(self,
            start_time: datetime,
            end_time: datetime,
            timestep: timedelta) -> bool:
        
        results = {
            'start_dt_utc': [],
            'end_dt_utc': [],
            'charged_energy_kwh': []
        }

        current_time = start_time
        while current_time <= end_time:
            if self.trigger_checker.is_triggered(current_time, results):
                schedules = self.optimizer.optimize_sessions(current_time)
                self.trigger_checker.update_schedules()
                

            results = self.charging_hub.charge(schedules)


            current_time += timestep

