from flask import Flask, render_template, request, jsonify
import json
import folium

## All service or other modules imports
from api.routes.ask import ask_service
from database.connection_interact_db import create_load_test_data_seerist
from services.normalization_service import *
from services.ingest_service import *
from services.map_all_events_service import *
from services.stats_services.macro_stats_service import macro_stats_service
from services.stats_services.time_charts_service import time_charts_event_count_memory, time_charts_stacked_volumes
from services.list_events_service import list_events_service
from services.show_location_map_service import show_location_map_service

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
    return list_events_service()

@app.route('/map/inspect')
def show_location_map():
    return show_location_map_service()



@app.route('/stats')
def stats():
    return render_template("stats.html")


@app.route('/stats/macro')
def macro_stats():
    return macro_stats_service()

@app.route('/stats/time_charts')
def time_charts():
    return render_template("time_charts.html", time_chart_event_count=time_charts_event_count_memory(), time_chart_stacked_volumes=time_charts_stacked_volumes())



@app.route('/test_folium')
def test_folium():
    m = folium.Map(location=[20, 0], zoom_start=2, tiles='CartoDB.Positron')

    return m._repr_html_()

if __name__ == '__main__':
    app.run(debug=True)