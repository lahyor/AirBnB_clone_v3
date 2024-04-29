#!/usr/bin/python3
"""This script """


from api.v1.views import app_views
from flask import jsonify
from models import storage
import json
from flask import request
from models.city import City
from flask import abort


@app_views.route("/states/<state_id>/cities", strict_slashes=False)
def show_cities(state_id):
    """Return all cities in state"""
    result = []
    for city in storage.all("City").items():
        if state_id == city[1].state_id:
            result.append(city[1].to_dict())
    if len(result) is 0:
        abort(404)
    return jsonify(result)


@app_views.route("/cities/<city_id>", strict_slashes=False)
def show_city(city_id):
    """Return a specifique City object or raise a 404 error"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route(
    "/cities/<city_id>",
    methods=['DELETE'],
    strict_slashes=False)
def delete_city(city_id):
    """Delete a specifique City object or raise a 404 error"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route(
    "/states/<state_id>/cities",
    methods=['POST'],
    strict_slashes=False)
def create_city(state_id):
    """Create a city """
    request_body = request.get_json()
    if not request.is_json:
        abort(400, description="Not a JSON")
    if "name" not in request_body:
        abort(400, description="Missing name")
    new_city = City(name=request_body.get("name"), state_id=state_id)
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=['PUT'], strict_slashes=False)
def update_city(state_id):
    """Update a city object or raise a 404 error"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    request_body = request.get_json()
    if not request.is_json:
        abort(400, description="Not a JSON")
    for key, value in request_body.items():
        if key not in ["id", "state_id", "created_at ", "updated_at"]:
            setattr(city, key, value)
    storage.save()
    return jsonify(city.to_dict()), 200
