import pandas as pd
from datetime import datetime, timedelta, timezone

from data.data_reader import DataReader

class EnergyForecastReader(DataReader):
    def __init__(self, db_connector):
        super().__init__(db_connector)

    def read(self,
             path: str = None,
             start_dt_utc: datetime = None,
             end_dt_utc: datetime = None) -> pd.DataFrame:
        
        if self.db_connector:
            return pd.DataFrame
        else:
            return self.generate_dummy_data(start_dt_utc, end_dt_utc)
        
    def generate_dummy_data(self, 
                            start_dt_utc: datetime = None, 
                            end_dt_utc: datetime = None
                            ) -> pd.DataFrame:
        pass
