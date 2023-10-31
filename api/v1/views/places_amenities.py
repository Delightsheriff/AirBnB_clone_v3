#!/usr/bin/python3
"""This returns the status of our api"""
from api.v1.views import app_views
from flask import jsonify, request, abort, make_response
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<string:place_id>/reviews',
                 strict_slashes=False, methods=['GET', 'POST'])
def get_all_place_reviews(place_id):
    """This performs tasks according to
    the request"""
    temp = storage.get(cls=Place, id=place_id)
    if not temp:
        abort(404)
    if request.method == 'GET':
        return jsonify([x.to_dict() for x in temp.reviews])
    elif request.method == 'POST':
        data = request.get_json()
        if data is None:
            return make_response(jsonify("Not a JSON"), 400)
        if 'user_id' not in data:
            return make_response(jsonify("Missing user_id"), 400)
        user = storage.get(cls=User, id=data['user_id'])
        if user is None:
            abort(404)
        if 'text' not in data:
            return make_response(jsonify("Missing text"), 400)
        data['place_id'] = place_id
        rev = Review(**data)
        rev.save()
        return make_response(jsonify(rev.to_dict()), 201)


@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['GET', 'PUT', 'DELETE'])
def work_with_review_id(review_id):
    """This function performs tasks according to the
    request"""
    temp = storage.get(cls=Review, id=review_id)
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
        for k, v in data.items():
            if k not in ['id', 'place_id', 'user_id',
                         'created_at', 'updated_at']:
                setattr(temp, k, v)
        temp.save()
        return make_response(jsonify(temp.to_dict()), 200)
