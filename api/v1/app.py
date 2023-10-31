#!/usr/bin/python3
"""AirBnB Clone API"""

# Import Flask and storage
from api.v1.views import app_views
from flask import Flask, make_response, jsonify
from models import storage
from os import getenv

app = Flask(__name__)
CORS = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_app(exception):
    """Close the storage session"""
    storage.close()


@app.errorhandler(404)
def not_found_404(error):
    """Handle non existing pages"""
    return make_response(jsonify({'error': "Not found"}), 404)


if __name__ == '__main__':
    host = getenv("HBNB_API_HOST", "0.0.0.0")
    port = getenv("HBNB_API_PORT", "5000")
    app.run(host=host, port=port)
