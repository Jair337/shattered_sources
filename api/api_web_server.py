from flask import Flask, render_template, request, jsonify

## All service or other modules imports
from database.connection_interact_db import create_load_test_data_seerist
from services.ingest_service import *
from services.map_all_events_service import *
from services.stats_services.macro_stats_service import macro_stats_service
from services.stats_services.time_charts_service import time_charts_event_count_memory, time_charts_stacked_volumes
from services.list_events_service import list_events_service
from services.show_location_map_service import show_location_map_service
from services.stats_services.custom_time_charts_service import custom_time_chart_service
from services.map_choropleth_service import generate_choropleth_map
from services.stats_services.distribution_charts_service import categories_distribution_chart_service
from services.stats_services.geographic_charts_service import country_chart_service
from services.machine_learning_service import ML_demo_random_forest
from services.ask_service import generate_query, get_db_scheme

app = Flask(__name__, template_folder='./html_templates')

## PATHS
@app.route('/')
def hello():
    return render_template("html_template_home.html")

#########################################################################################################################################################################################################################
@app.route('/insert_data')
def insert_data():
    create_load_test_data_seerist()
    return "yay"

@app.route('/normalize_ingest_seerist', methods=['POST']) ## Logic that normalizes and ingests the seerist data into the normalized db, and saves a copy of the raw data to raw seerist events
def ingest_seerist_api():

    raw_data = request.get_json()
    result = ingest_seerist(raw_data)

    if result[0] == 'Success':
        return jsonify(result)

    else:
        return "error"


#########################################################################################################################################################################################################################

@app.route("/map/events")
def render_map_events_endpoint():
    ## Pulls events from normalized DB and puts them into a interactive map.
    return render_map_events()

@app.route("/map/choropleth")
def render_map_choropleth():
    return generate_choropleth_map()


@app.route('/map/inspect')
def show_location_map():
    return show_location_map_service()


#########################################################################################################################################################################################################################


@app.route('/events_list')
## Pulls all events from normalized DB and puts them into a interactive list
def list_events():
    return list_events_service()


#########################################################################################################################################################################################################################

@app.route('/stats')
def stats():
    return render_template("stats.html")


@app.route('/stats/macro')
def macro_stats():
    return macro_stats_service()

@app.route('/stats/time_charts')
def time_charts():
    return render_template("time_charts.html", time_chart_event_count=time_charts_event_count_memory(), time_chart_stacked_volumes=time_charts_stacked_volumes())

@app.route('/stats/time_charts_custom', methods=['POST', 'GET'])
def time_charts_custom():
    chosen_country = None
    if request.method == 'POST':
        chosen_country = request.form['country']
    data_country_selected = custom_time_chart_service(chosen_country)
    return render_template("time_charts_custom.html", chart_data=data_country_selected[0], countries=data_country_selected[1], selected_country=data_country_selected[2])

@app.route('/stats/distribution_charts')
def distribution_charts():
    return render_template("distribution_charts.html", category_chart = categories_distribution_chart_service())


@app.route('/stats/geographic_charts')
def geographic_charts():
    return render_template("geographic_charts.html", geographic_chart = country_chart_service())


##########################################################################################################################################################################################


@app.route('/machine_learning')
def machine_learning():
    return render_template("machine_learning.html")

@app.route('/train', methods=['GET'])
def train_model():
    mae, r2, residuals, cm, accuracy, precision, recall, f1, predictions, y_test = ML_demo_random_forest()
    print(r2)
    return jsonify({
        "mae": mae,
        "r2": round(r2, 2),
        "predictions": [
            {"id": i + 1, "actual": round(act, 2), "predicted": round(pred, 2)}
            for i, (act, pred) in enumerate(zip(y_test.tolist(), predictions.tolist()))
        ]

    })

@app.route('/view_test_data')
def view_test_data():
    return render_template("view_test_data.html")


##########################################################################################################################################################################################



@app.route('/ask_llm')
def ask_llm():
    return render_template("ask_llm.html")


@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_question = data.get("question", "")

    sql_query = generate_query(user_question, get_db_scheme())
    print(sql_query)

    with sqlite3.connect(db_path_normalized) as conn:
         cursor = conn.cursor()
         cursor.execute(sql_query)
         results = cursor.fetchall()
         print(results)

    return jsonify({"results": results})


#########################################################################################################################################################################################################################
if __name__ == '__main__':
    app.run(debug=True)