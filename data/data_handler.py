from abc import ABC, abstractmethod
from datetime import datetime
import pandas as pd


class DataHandler(ABC):
    def __init__(self,
                 db_connector: object):
        self.db_connector = db_connector
    
    @abstractmethod
    def read(self,
             path: str = None,
             start_dt_utc: datetime = None,
             end_dt_utc: datetime = None) -> pd.DataFrame:
        pass

