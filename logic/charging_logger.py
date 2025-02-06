import pandas as pd
from datetime import datetime

class ChargingLogger:
    def __init__(self, batch_size=1000):
        """Initialize a list for batching and an empty DataFrame for storage."""
        self.records = pd.DataFrame(columns=["timestamp", "charging_data"])
        self.buffer = []  
        self.batch_size = batch_size  

    def log(self, 
            timestamp: datetime, 
            charging_data: pd.DataFrame):
        self.buffer.append({"timestamp": timestamp, "charging_data": charging_data})

        if len(self.buffer) >= self.batch_size:
            self.flush_to_dataframe() 

    def flush_to_dataframe(self):
        if self.buffer:
            new_entries = pd.DataFrame(self.buffer)
            self.records = pd.concat([self.records, new_entries], ignore_index=True)
            self.buffer = [] 

    def get_logs(self) -> pd.DataFrame:
        self.flush_to_dataframe()
        return self.records
