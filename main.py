from flask import Flask
from api import *
from api.api_web_server import app

if __name__ == "__main__":
    app.run(debug=True)