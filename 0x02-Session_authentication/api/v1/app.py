#!/usr/bin/env python3
"""
Module for the API routes and app.
"""
from api.v1.views import app_views
from flask import Flask, jsonify, abort
from os import getenv
from api.v1.auth.basic_auth import BasicAuth
from flask import request


app = Flask(__name__)
app.register_blueprint(app_views)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

auth = None

if getenv('AUTH_TYPE') == 'basic_auth':
    auth = BasicAuth()

@app.before_request
def before_request():
    """Before request handler
    """
    if auth is not None:
        request.current_user = auth.current_user(request)

@app.errorhandler(404)
def not_found(error) -> str:
    """Not found handler
    """
    return jsonify({'error': 'Not found'}), 404

if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port, debug=True)
