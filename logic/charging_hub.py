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
               timestep: timedelta) -> pd.DataFrame:
        # Retrieve available energy
        meter_values = self.smart_meter.get_meter_values(current_dt_utc, current_dt_utc + timestep)
        available_energy_kwh = meter_values["energy_kwh"] + (self.max_gridpower_kw * timestep.total_seconds() / 3600)
                                   
        charging_cars = self.get_charging_cars(current_dt_utc)

        # Merge signals with charging cars
        active_signals = signals.merge(charging_cars, on="car_id", how="inner")

        if active_signals.empty:
            return pd.DataFrame(columns=["car_id", "charged_energy_kwh"])

        # Ensure no car gets more than its target
        active_signals["max_possible_kwh"] = active_signals["target_energy_kwh"] - active_signals["charged_energy_kwh"]
        active_signals["energy_request_kwh"] = active_signals[["energy_kwh", "max_possible_kwh"]].min(axis=1)

        total_requested = active_signals["energy_request_kwh"].sum()

        # Distribute energy proportionally
        if total_requested > available_energy_kwh:
            scaling_factor = available_energy_kwh / total_requested
            active_signals["charged_energy_kwh"] = active_signals["energy_request_kwh"] * scaling_factor
        else:
            active_signals["charged_energy_kwh"] = active_signals["energy_request_kwh"]

        # Update session records
        self.sessions.loc[self.sessions["car_id"].isin(active_signals["car_id"]),
                          "charged_energy_kwh"] += active_signals["charged_energy_kwh"]

        return active_signals[["car_id", "charged_energy_kwh"]]

    def get_charging_cars(self, current_time: datetime) -> pd.DataFrame:
        return self.sessions[
            (self.sessions["start_dt_utc"] <= current_time) &
            (self.sessions["end_dt_utc"] > current_time) &
            (self.sessions["charged_energy_kwh"] < self.sessions["target_energy_kwh"])
        ]
