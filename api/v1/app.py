#!/usr/bin/python3
"""This is the entry to the api"""

from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS
import json
from flask import jsonify
from werkzeug.exceptions import BadRequest
from flasgger import Swagger
from flasgger.utils import swag_from

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(app_views)
CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})



@app.teardown_appcontext
def close_storage(exception):
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Handler for 404 errors that returns a
    JSON-formatted 404 status code response"""
    return jsonify({"error": "Not found"}), 404


app.config['SWAGGER'] = {
    'title': 'AirBnB clone Restful API',
    'uiversion': 3
}

Swagger(app)


if __name__ == "__main__":
    api_host = getenv("HBNB_API_HOST", "0.0.0.0")
    api_port = getenv("HBNB_API_PORT", 5000)
    app.run(host=api_host, port=api_port, threaded=True)
