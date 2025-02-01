import os

from data.session_handler import SessionHandler
from common.helper_functions import run_local



if run_local:
    database_connector = None
else:
    pass

session_handler = SessionHandler(database_connector)
current_sessions = session_handler.read()
print(current_sessions)
