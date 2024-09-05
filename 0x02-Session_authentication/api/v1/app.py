#!/usr/bin/env python3
""" API module """
from os import getenv
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from flask_cors import CORS
from api.v1.auth.basic_auth import BasicAuth
from api.v1.auth.session_auth import SessionAuth  # Import SessionAuth

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

# Choose auth mechanism based on environment variable
auth = None
auth_type = getenv('AUTH_TYPE')
if auth_type == 'basic_auth':
    auth = BasicAuth()
elif auth_type == 'session_auth':
    auth = SessionAuth()  # Assign SessionAuth instance

@app.teardown_appcontext
def close_db(error):
    """ Close the database session at the end of the request """
    storage.close()

@app.errorhandler(404)
def not_found(error):
    """ 404 Error Handler """
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(401)
def unauthorized(error):
    """ 401 Unauthorized Error Handler """
    return jsonify({"error": "Unauthorized"}), 401

@app.errorhandler(403)
def forbidden(error):
    """ 403 Forbidden Error Handler """
    return jsonify({"error": "Forbidden"}), 403

if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = int(getenv("API_PORT", 5000))
    app.run(host=host, port=port)

