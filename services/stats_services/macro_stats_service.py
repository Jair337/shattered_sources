import sqlite3
from flask import render_template
from config import db_path_normalized


def macro_stats_service():
    with sqlite3.connect(db_path_normalized) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM events_normalized")
        total_events = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM events_normalized WHERE severity >= 4")
        high_severity_events = cursor.fetchone()[0]
        threat_percentage = round(high_severity_events/total_events * 100)

        cursor.execute("SELECT COUNT(DISTINCT city) FROM events_normalized")
        unique_cities = cursor.fetchone()[0]

    return render_template("macro_stats.html", total_volume=total_events, threat_percentage=threat_percentage, unique_cities=unique_cities)
