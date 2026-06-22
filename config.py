import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

## Forces the path to be the right one
db_path_seerist = os.path.join(BASE_DIR, 'database', 'events_seerist_raw.db')
db_path_normalized = os.path.join(BASE_DIR, 'database', 'events_normalized.db')
json_path = os.path.join(BASE_DIR, 'synthetic_seerist_events.json')