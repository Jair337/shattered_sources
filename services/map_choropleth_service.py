import sqlite3
import folium
import pandas as pd
from config import db_path_normalized

def generate_choropleth_map():
    with sqlite3.connect(db_path_normalized) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT country, COUNT(*) AS event_count
            FROM events_normalized
            GROUP BY country
        """)
        data = cursor.fetchall()
        print(data)


    ## Pulls the country borders
    geo_json_url = "https://raw.githubusercontent.com/python-visualization/folium/main/examples/data/world-countries.json"

    m = folium.Map(location=[20, 0], zoom_start=2, tiles="CartoDB positron")

    folium.Choropleth(
        geo_data=geo_json_url,
        data=pd.DataFrame(data, columns=["country", "event_count"]),
        columns=["country", "event_count"],
        key_on="feature.properties.name",
        fill_color="YlOrRd",  # Yellow to Orange to Red gradient
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name="Database Event Counts",
        nan_fill_color="#1c2d42"
    ).add_to(m)

    return  m._repr_html_()
