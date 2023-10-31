#!/usr/bin/python3
"""This returns the status of our api"""
from api.v1.views import app_views
from flask import jsonify, request, abort, make_response
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.state import State


@app_views.route('/cities/<string:city_id>/places',
                 strict_slashes=False, methods=['GET', 'POST'])
def get_all_city_places(city_id):
    """Retrieves the list of all Place objects of a city"""
    temp = storage.get(cls=City, id=city_id)
    if not temp:
        abort(404)
    if request.method == 'GET':
        return jsonify([x.to_dict() for x in temp.places])
    elif request.method == 'POST':
        data = request.get_json()
        if data is None:
            return make_response(jsonify("Not a JSON"), 400)
        if 'name' not in data:
            return make_response(jsonify("Missing name"), 400)
        data['city_id'] = city_id
        place = Place(**data)
        place.save()
        return make_response(jsonify(place.to_dict()), 201)


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['GET', 'PUT', 'DELETE'])
def work_with_place_id(place_id):
    """Delete and UPDATES a Place object"""
    temp = storage.get(cls=Place, id=place_id)
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
            if i not in ['id', 'user_id', 'city_id',
                         'created_at', 'updated_at']:
                setattr(val, i, j)
        temp.save()
        return make_response(jsonify(temp.to_dict()), 200)


@app_views.route('/places_search', strict_slashes=False, methods=['POST'])
def place_search():
    """Creates a Place object"""
    data = request.get_json()
    if data is None:
        return make_response(jsonify("Not a valid JSON"), 400)
    cities = data.get('cities', None)
    states = data.get('states', None)
    amen_s = data.get('amenities', None)
    if not data or not len(data) or (
            not states and
            not cities and
            not amen_s):
        return jsonify([i.to_dict() for i in storage.all(Place).values()])
    temp_places = []
    if states:
        temp_states = [storage.get(State, s_id) for s_id in states]
        for state in temp_states:
            if state:
                for city in state.cities:
                    if city:
                        for place in city.places:
                            temp_places.append(place)
    if cities:
        temp_cities = [storage.get(City, c_id) for c_id in cities]
        for city in temp_cities:
            if city:
                for place in city.places:
                    temp_places.append(place)
    temp_places = [x for x in temp_places if x is not None]
    if amen_s:
        l_amen_s = [storage.get(Amenity, a_id) for a_id in amen_s]
        if not temp_places:
            temp_places = storage.all(Place).values()
        l_amen = [x for x in l_amen_s if x is not None]
        temp_places = [x for x in temp_places if all(
            mem in x.amenities for mem in l_amen)]
    places = []
    for place in temp_places:
        dict_ = place.to_dict()
        dict_.pop('amenities', None)
        places.append(dict_)
    return jsonify(places)
