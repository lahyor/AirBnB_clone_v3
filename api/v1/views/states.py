#!/usr/bin/python3
"""This script """


from api.v1.views import app_views
from flask import jsonify
from models import storage
import json
from flask import request
from models.state import State
from flask import abort


@app_views.route("/states/", strict_slashes=False)
def show_states():
    """Return all states objets"""
    result = []
    for state in storage.all("State").items():
        result.append(state[1].to_dict())
    return jsonify(result)


@app_views.route("/states/<state_id>", strict_slashes=False)
def show_state(state_id):
    """Return a specifique State object or raise a 404 error"""
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route(
    "/states/<state_id>",
    methods=['DELETE'],
    strict_slashes=False)
def delete_state(state_id):
    """Delete a specifique State object or raise a 404 error"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route("/states", methods=['POST'], strict_slashes=False)
def create_state():
    request_body = request.get_json()
    if not request.is_json:
        abort(400, description="Not a JSON")
    if "name" not in request_body:
        abort(400, description="Missing name")
    state = State(name=request_body.get("name"))
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route("/states/<state_id>", methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Return a specifique State object or raise a 404 error"""
    state = storage.get("State", state_id)
    request_body = request.get_json()
    if state is None:
        abort(404)
    if not request.is_json:
        abort(400, description="Not a JSON")
    if "name" not in request_body:
        abort(400)
    for key, value in request_body.items():
        if key not in ["id", "created_at", "updates_at"]:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200
