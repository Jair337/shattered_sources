# Needs to have logic that reads what kind of event it is and calls to that one accordingly
from config import *
from services.normalization_service import *
import sqlite3
import json


def ingest_seerist(raw_data):
    ## Runs the normalization service and returns the event in json


    ## Save the raw data to the raw seerist events table
    with sqlite3.connect(db_path_seerist) as conn:
        for event in raw_data:
            record = (
                event.get('event_id'),
                event.get('kind'),
                event.get('title'),
                event.get('summary'),
                event.get('category'),
                event.get('sub_category'),
                event.get('severity'),
                event.get('severity_label'),
                event.get("status"),
                event.get("confidence"),
                event.get("published_at"),
                event.get("updated_at"),
                event.get("start_time"),
                event.get("end_time"),
                event.get("region"),
                event.get("language"),
                event.get("raw_text"),

                ## Nested data intact as JSON string
                json.dumps(event.get("location", {})),
                json.dumps(event.get("provenance", {})),
                json.dumps(event.get("impact", {})),
                json.dumps(event.get("tags", [])),
                json.dumps(event.get("assets_nearby", [])))

            conn.execute("""INSERT OR REPLACE INTO events_seerist_raw VALUES 
                    (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", record)

    normalized_event = normalize_event_seerist(raw_data)
