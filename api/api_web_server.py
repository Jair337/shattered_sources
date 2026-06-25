from flask import Flask, render_template, request, jsonify
import json
import folium
from fontTools.misc.cython import returns

## All service or other modules imports
from api.routes.ask import ask_service
from database.connection_interact_db import create_load_test_data_seerist
from services.normalization_service import *
from services.ingest_service import *
from services.map_all_events_service import *
from services.stats_services.macro_stats_service import macro_stats_service

app = Flask(__name__, template_folder='./html_templates')

## PATHS
@app.route('/')
def hello():
    return render_template("html_template_home.html")

@app.route('/ask')
def ask_route():
    return ask_service()
@app.route('/insert_data')
def insert_data():
    create_load_test_data_seerist()
    return "yay"



@app.route("/map/events")
def render_map_events_endpoint():
    ## Pulls events from normalized DB and puts them into a interactive map.
    return render_map_events()





@app.route('/normalize_ingest_seerist', methods=['POST']) ## Logic that normalizes and ingests the seerist data into the normalized db, and saves a copy of the raw data to raw seerist events
def ingest_seerist_api():

    raw_data = request.get_json()
    result = ingest_seerist(raw_data)

    if result[0] == 'Success':
        return jsonify(result)

    else:
        return "error"

@app.route('/events_list')
## Pulls all events from normalized DB and puts them into a interactive list
def list_events():
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

@app.route('/map/inspect')
def show_location_map():
    ## Pulls events from normalized DB and puts them into a interactive map.
    ## NOTE = The logic here and in the HTML file is written by me,
    ## however AI was used for the HTML part and the parts surrounding the logic that creates the map.
    lat = request.args.get('lat')
    lng = request.args.get('lon')
    event_title = request.args.get('title')

    custom_popup = folium.Popup(
        html=f"<b>{event_title}</b>",
        max_width=450)

    m = folium.Map(location=[float(lat), float(lng)], zoom_start=11, tiles='CartoDB.Positron')
    (folium.Marker(location=[float(lat), float(lng)],
                  tooltip='Click for more info',
                  popup=custom_popup,
                  icon=folium.Icon(color="red")
                   ) .add_to(m))

    return m._repr_html_()

@app.route('/stats/macro')
def macro_stats():
    return macro_stats_service()


@app.route('/stats')
def stats():
    return render_template("stats.html")
@app.route('/test_folium')
def test_folium():
    m = folium.Map(location=[20, 0], zoom_start=2, tiles='CartoDB.Positron')

    return m._repr_html_()

if __name__ == '__main__':
    app.run(debug=True)