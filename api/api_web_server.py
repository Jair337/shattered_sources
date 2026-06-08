from flask import Flask, render_template

## All service or other modules imports
from api.routes.ask import ask_service
from database.connection_interact_db import create_load_test_data_seerist

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

if __name__ == '__main__':
    app.run(debug=True)