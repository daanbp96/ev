import random
import pandas as pd
import os
from datetime import datetime, timezone, timedelta, date

from data.data_reader import DataReader

class SessionReader(DataReader):
    def __init__(self, db_connector: object):
        super().__init__(db_connector)

    def read(self, 
             path: str = None, 
             start_dt_utc: datetime = None, 
             end_dt_utc: datetime = None
             ) -> pd.DataFrame:
        """Reads the energy data, either from a database or generates dummy data."""
        if os.getenv("USE_DUMMY_DATA", "False").lower() == "true":
            sessions = self._generate_dummy_data(start_dt_utc, end_dt_utc)
        else:
            sessions = pd.DataFrame()
        if os.getenv("DEBUG_MODE", "False").lower() == "true":
            print("Session data:")
            print(f"Start datetime (UTC): {sessions['start_dt_utc'].min()}")
            print(f"Last start datetime (UTC): {sessions['start_dt_utc'].max()}")
            print(f"Number of unique cars: {sessions['car_id'].nunique()}")
            print(f"Total number of sessions: {len(sessions)}")            
        return sessions 
            

    def _generate_dummy_data(self, 
                            start_dt_utc: datetime = None, 
                            end_dt_utc: datetime = None, 
                            number_of_sessions: int = 20,
                            number_of_unique_cars: int = 5
                            ) -> pd.DataFrame:
        if not start_dt_utc:
            start_dt_utc = datetime.now(timezone.utc) - timedelta(days=7)
        if not end_dt_utc:
            end_dt_utc = datetime.now(timezone.utc)

        total_days = (end_dt_utc - start_dt_utc).days
        max_sessions = min(number_of_sessions, number_of_unique_cars * total_days)
        if number_of_sessions > max_sessions:
            print(f'number of sessions higher than allowed. It is reduced to {max_sessions}')

        prob_of_session_per_day = (number_of_sessions / (number_of_unique_cars * total_days))
        car_ids = [f"CAR-{i}" for i in range(1, number_of_unique_cars + 1)]
        car_last_sessions = {}  # Track last session per car

        data = []
        for day in range(total_days):
            session_start_day = start_dt_utc + timedelta(days=day)
            for car_id in car_ids:
                if self.session_today(prob_of_session_per_day):  # Should car charge today?
                    session_start = self._get_biased_session_start(session_start_day)

                    # Ensure no overlapping sessions
                    last_session = car_last_sessions.get(car_id)
                    if last_session and last_session["end_dt_utc"] > session_start:
                        session_start = last_session["end_dt_utc"] + timedelta(minutes=random.randint(15, 60))

                    session_end = session_start + timedelta(hours=random.uniform(3, 8))  # Sessions last between 3-8 hours
                    if session_end > end_dt_utc:
                        session_end = end_dt_utc

                    charged_kwh = round(random.uniform(10, 80), 2)  # Random energy charged

                    session = {
                        "car_id": car_id,
                        "session_id": f"SESSION-{random.randint(100000, 999999)}",
                        "start_dt_utc": session_start,
                        "end_dt_utc": session_end,
                        "charged_energy_kwh": charged_kwh,
                        "target_energy_kwh": 0
                    }

                    data.append(session)
                    car_last_sessions[car_id] = session  # Update last session per car

        return pd.DataFrame(data)

    def session_today(self, prob: float) -> bool:
        """Returns True with probability `prob` (e.g., 0.2 for 20% chance)."""
        return random.random() < prob

    def _get_biased_session_start(self, start_day: date) -> datetime:
        """Generates a session start time with 75% probability between 08:00-20:00."""
        if random.random() < 0.75:
            hour = random.randint(8, 19)  # 08:00-19:59 (75% chance)
        else:
            hour = random.choice(list(range(0, 8)) + list(range(20, 24)))  # 00:00-07:59 or 20:00-23:59 (25% chance)

        return datetime.combine(start_day, datetime.min.time(), tzinfo=timezone.utc) + timedelta(
            hours=hour, minutes=random.randint(0, 59)
        )
