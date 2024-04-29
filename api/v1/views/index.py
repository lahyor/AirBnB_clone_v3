#!/usr/bin/python3
"""
This script containe the blueprint routes
"""


from api.v1.views import app_views
from flask import jsonify
from models import storage
import json


@app_views.route("/status", strict_slashes=False)
def status():
    """Returns a json response"""
    return jsonify(status="OK")
