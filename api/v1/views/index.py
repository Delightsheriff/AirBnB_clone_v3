#!/usr/bin/python3
"""API index"""
# Import app_views from api.v1.views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from api.v1.views import app_views
from flask import jsonify


# Create a route /status on the object app_views returns JSON: "status": "OK"
@app_views.route('/status')
def status():
    """Return a JSON with status OK"""
    temp = {
        "status": "OK"
    }
    return jsonify(temp)


@app_views.route('/stats', strict_slashes=False)
def stats():
    """Retrieves the number of each objects by type"""
    temp = {}
    temp['amenities'] = storage.count(Amenity)
    temp['cities'] = storage.count(City)
    temp['places'] = storage.count(Place)
    temp['reviews'] = storage.count(Review)
    temp['states'] = storage.count(State)
    temp['users'] = storage.count(User)
    return jsonify(temp)
