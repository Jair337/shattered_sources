# Needs to have logic that reads what kind of event it is and calls to that one accordingly
from config import *
from services.normalization_service import *
import sqlite3
import json


########################################################################################################################################################
# Ingest service # Takes in the raw data, saves it to the raw seerist events table, and then normalizes it and saves it to the normalized events table #
########################################################################################################################################################

def ingest_seerist(raw_data):
    ## Save the raw data to the raw seerist events table
    with sqlite3.connect(db_path_seerist) as conn:
            record = (
                raw_data.get('event_id'),
                raw_data.get('kind'),
                raw_data.get('title'),
                raw_data.get('summary'),
                raw_data.get('category'),
                raw_data.get('sub_category'),
                raw_data.get('severity'),
                raw_data.get('severity_label'),
                raw_data.get("status"),
                raw_data.get("confidence"),
                raw_data.get("published_at"),
                raw_data.get("updated_at"),
                raw_data.get("start_time"),
                raw_data.get("end_time"),
                raw_data.get("region"),
                raw_data.get("language"),
                raw_data.get("raw_text"),

                ## Nested data intact as JSON string
                json.dumps(raw_data.get("location", {})),
                json.dumps(raw_data.get("provenance", {})),
                json.dumps(raw_data.get("impact", {})),
                json.dumps(raw_data.get("tags", [])),
                json.dumps(raw_data.get("assets_nearby", [])))

            conn.execute("""INSERT OR REPLACE INTO events_seerist_raw VALUES 
                    (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", record)

    ## Enters the normalized event into the normalized DB
    normalized_event = normalize_event_seerist(raw_data)
    with sqlite3.connect(db_path_normalized) as conn_n:
        conn_n.execute("""INSERT OR REPLACE INTO events_normalized (
         normalized_event_id, original_event_id, source_name, event_type, title, description, category, 
            severity, confidence, time_stamp, country, region, city, latitude, longitude)
         VALUES (
            :normalized_event_id, :original_event_id, :source_name, :event_type, :title, :description, :category, 
            :severity, :confidence, :time_stamp, :country, :region, :city, :latitude, :longitude)""", normalized_event)

    return "Success", "normalized_id: " + str(normalized_event["normalized_event_id"]) + " has been processed"
