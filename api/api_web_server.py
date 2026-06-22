from flask import Flask, render_template, request

## All service or other modules imports
from api.routes.ask import ask_service
from database.connection_interact_db import create_load_test_data_seerist
from services.normalization_service import *

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



@app.route('/normalize_ingest_seerist', methods=['POST']) ## Logic that normalizes and ingests the seerist data into the normalized db, and saves a copy of the raw data to raw seerist events
def ingest_seerist():
    raw_data = request.get_json()

    ingest_seerist(raw_data)


    return "Event normalized and ingested successfully"

if __name__ == '__main__':
    app.run(debug=True)