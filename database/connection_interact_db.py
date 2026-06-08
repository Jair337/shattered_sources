import sqlite3
import json
import os

#imports the paths from config
from config import *



## function that imports and stores all the seerist test data.
def create_load_test_data_seerist():
    ## Import path of json and db from config file
    path_json = json_path
    path_db = db_path_seerist

    ## Check if json or db path exists
    if not os.path.exists(path_json):
        return(f"Error: {path_json} does not exist")

    if not os.path.exists(path_db):
        return(f"Error: {path_db} does not exist")

    ## Reads the json file
    with open(path_json, 'r') as f:
        data = json.load(f)

    ## Gets the list of events
    events = data['events']

    print(f"{len(events)} events found")

    ## Transform data into tuples for insertion into DB
    ## note: Test data has fields like source, schema_version and synthetic notice. These are not imported into the DB
    processed_records = []
    for event in events:
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
            json.dumps(event.get("assets_nearby", []))
        )
        processed_records.append(record)

    ## Connect to DB
    with sqlite3.connect(path_db) as conn:
        cursor = conn.cursor()

        ## Create tables
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS events_seerist_raw (
            event_id TEXT PRIMARY KEY,
            kind TEXT,
            title TEXT,
            summary TEXT,
            category TEXT,
            sub_category TEXT,
            severity TEXT,
            severity_label TEXT,
            status TEXT,
            confidence TEXT,
            published_at TEXT,
            updated_at TEXT,
            start_time TEXT,
            end_time TEXT,
            region TEXT,
            language TEXT,
            raw_text TEXT,
            location TEXT,
            provenance TEXT,
            impact TEXT,
            tags TEXT,
            assets_nearby TEXT
        )      
        ''')

        ## Defines the query for inserting into the DB
        ## The ?s are to prevent SQL injection by preventing direct variable input in the string
        query = '''
                    INSERT OR REPLACE INTO events_seerist_raw VALUES 
                    (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                '''
        cursor.executemany(query, processed_records)
        conn.commit()

    print(f"{len(processed_records)} records written to {path_db}")




## MUST WRITE CODE THAT PULLS NEW ALERTS EVERY N SECONDS AND ADDS THEM TO DB --> NEW ALERTS -- PLOTTED AGAINST MODEL --> ADDED TO MAIN DB WITH EITHER REQUIRES ATTENTION OR NOT