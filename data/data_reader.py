from abc import ABC, abstractmethod
import os
from datetime import datetime
import pandas as pd


class DataReader(ABC):
    def __init__(self,
                 db_connector: object):
        self.db_connector = db_connector
    
    def read(self, 
             path: str = None, 
             start_dt_utc: datetime = None, 
             end_dt_utc: datetime = None
             ) -> pd.DataFrame:
        """Reads the energy data, either from a database when no db connector provided it generates dummy data."""
        if os.getenv("USE_DUMMY_DATA", "False").lower() == "true":
            return self._generate_dummy_data(start_dt_utc, end_dt_utc)
        else:
            return pd.DataFrame()
        
    @abstractmethod
    def _generate_dummy_data(self,
                                 start_dt_utc: datetime,
                                 end_dt_utc: datetime):
        pass

