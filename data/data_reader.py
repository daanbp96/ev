from abc import ABC, abstractmethod
import os
from datetime import datetime
import pandas as pd


class DataReader(ABC):
    def __init__(self,
                 db_connector: object):
        self.db_connector = db_connector
        
    @abstractmethod
    def _generate_dummy_data(self,
                                 start_dt_utc: datetime,
                                 end_dt_utc: datetime):
        pass

