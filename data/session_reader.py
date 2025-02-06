import random
import pandas as pd
from datetime import datetime, timezone, timedelta

from data.data_reader import DataReader

class SessionReader(DataReader):
    def __init__(self, db_connector: object):
        super().__init__(db_connector)
    
    def _generate_dummy_data(self, 
                            start_dt_utc: datetime = None, 
                            end_dt_utc: datetime = None
                            ) -> pd.DataFrame:
        num_sessions = 20  
        data = []
        
        if not start_dt_utc:
            start_dt_utc = datetime.now(timezone.utc) - timedelta(days=7)
        if not end_dt_utc:
            end_dt_utc = datetime.now(timezone.utc)
        
        for _ in range(num_sessions):
            car_id = f"CAR-{random.randint(1000, 9999)}"
            session_id = f"SESSION-{random.randint(100000, 999999)}"
            
            session_start = start_dt_utc + timedelta(seconds=random.randint(0, int((end_dt_utc - start_dt_utc).total_seconds())))
            session_end = session_start + timedelta(hours=random.uniform(1, 12))
            if session_end > end_dt_utc:
                session_end = end_dt_utc
            
            charged_kwh = round(random.uniform(10, 80), 2)
            
            data.append({
                "car_id": car_id,
                "session_id": session_id,
                "start_dt_utc": session_start,
                "end_dt_utc": session_end,
                "charged_kwh": charged_kwh
            })
        
        return pd.DataFrame(data)
