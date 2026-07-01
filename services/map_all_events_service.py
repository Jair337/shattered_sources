import sqlite3
import folium
from folium.plugins import MarkerCluster

from config import db_path_normalized


def render_map_events():
    with sqlite3.connect(db_path_normalized) as conn:
        ## DB connection that pulls all events and translates them into a dict
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM events_normalized ORDER BY time_stamp DESC")
        columns = [desc[0] for desc in cursor.description]
        raw_rows = cursor.fetchall()
        events = [dict(zip(columns, row)) for row in raw_rows]

        ## Makes the map and goes through every event and adds a marker to the map with a color based on severity. Red = 4+, Yellow = 3, Green = 1
        m = folium.Map(location=[20, 0], zoom_start=2, tiles='CartoDB.Positron', prefer_canvas=True)
        marker_cluster = MarkerCluster().add_to(m)
        for event in events:
            lat = event.get('latitude')
            lon = event.get('longitude')
            title = event.get('title')
            severity = event.get('severity')

            if severity >= 4:
                pin_color = "red"
            elif severity == 3:
                pin_color = "orange"
            else:
                pin_color = "green"

            ## Create simple HTML strings for the popup content, improves speed.
            popup_html = f'<div style="white-space: nowrap; font-weight: bold;">{title}</div>'

            ## Use CircleMarker instead of Marker. It utilizes the canvas and renders instantly.
            folium.CircleMarker(
                location=[float(lat), float(lon)],
                radius=6,
                color=pin_color,
                fill=True,
                fill_color=pin_color,
                fill_opacity=0.7,
                tooltip='Click for more info',
                popup=popup_html
            ).add_to(marker_cluster)

    return m._repr_html_()