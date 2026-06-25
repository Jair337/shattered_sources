import sqlite3
from flask import render_template
from config import db_path_normalized

def list_events_service():
    ## Currently comes into the logic as DB tuple, needs to be dict for list
    with sqlite3.connect(db_path_normalized) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM events_normalized ORDER BY time_stamp DESC")
        raw_rows = cursor.fetchall()

        ## Builds the columns as list
        columns = [desc[0] for desc in cursor.description]

        ## Turns every tuple row into dict, using the columns
        events = [dict(zip(columns, row)) for row in raw_rows]

    return render_template("events_list.html", events=events)