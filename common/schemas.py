
session = {
    "car_id": "string",
    "session_id": "string",
    "start_dt_utc": "datetime64[ns]",
    "end_dt_utc": "datetime64[ns]",
    "charging_speed_kw": "float64",
    "charged_energy_kwh": "float64",
    "target_energy_kwh": "float64",
    }

meter_value = {'start_dt_utc': "datetime64[ns]",
               'end_dt_utc': "datetime64[ns]",
               'meter_energy_kwh': "float64"
               }

energy_forecast = {'start_dt_utc': "datetime64[ns]",
                   'end_dt_utc': "datetime64[ns]",
                   'forecasted_energy_kwh': "float64"
                   }
signal = {
    "car_id": "string",
    'start_dt_utc': "datetime64[ns]",
    'end_dt_utc': "datetime64[ns]",
    'signal_energy_kwh': "float64"
    }