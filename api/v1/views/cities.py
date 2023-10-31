#!/usr/bin/python3
"""Create a new view for city"""

from flask import Flask, jsonify, request, abort, make_response
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<string:state_id>/cities',
                 strict_slashes=False, methods=['GET', 'POST'])
def get_all_state_cities(state_id):
    """This performs tasks according to the request received"""
    temp = storage.get(cls=State, id=state_id)
    if not temp:
        abort(404)
    if request.method == 'GET':
        return jsonify([x.to_dict() for x in temp.cities])
    elif request.method == 'POST':
        data = request.get_json()
        if data is None:
            return make_response(jsonify("Not a JSON"), 400)
        if 'name' not in data:
            return make_response(jsonify("Missing name"), 400)
        data['state_id'] = state_id
        city = City(**data)
        city.save()
        return make_response(jsonify(city.to_dict()), 201)


@app_views.route('/cities/<city_id>', strict_slashes=False,
                 methods=['GET', 'PUT', 'DELETE'])
def work_with_city_id(city_id):
    """This function performs tasks according to the request received"""
    temp = storage.get(cls=City, id=city_id)
    if not temp:
        abort(404)
    if request.method == 'GET':
        return jsonify(temp.to_dict())
    elif request.method == "DELETE":
        temp.delete()
        storage.save()
        return make_response(jsonify({}), 200)
    elif request.method == 'PUT':
        data = request.get_json()
        if data is None:
            return make_response(jsonify("Not a JSON"), 400)
        for i, j in data.items():
            if i not in ['id', 'state_id', 'created_at', 'updated_at']:
                setattr(temp, i, j)
        temp.save()
        return make_response(jsonify(temp.to_dict()), 200)
