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
def count():
    """retrieves the number of each objects by type"""

    avail_mod = {
        "User": "users",
        "Amenity": "amenities",
        "City": "cities",
        "Place": "places",
        "Review": "reviews",
        "State": "states",
    }
    model_objs = [Amenity, City, Place, Review, State, User]

    count = {}
    i = -1
    for temp in avail_mod.keys():
        i += 1
        count[avail_mod[temp]] = storage.count(model_objs[i])

    return jsonify(count)
