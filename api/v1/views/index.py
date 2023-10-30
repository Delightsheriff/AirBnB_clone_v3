#!/usr/bin/python3
"""API index"""
# Import app_views from api.v1.views
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
