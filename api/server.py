from flask import Flask
from fontTools.misc.cython import returns

from api.routes.ask import ask_service




app = Flask(__name__)
@app.route('/home')
def hello_world():
    return 'Hello World!'

@app.route('/ask')
def ask_route():
    return ask_service()

if __name__ == '__main__':
    app.run(debug=True)