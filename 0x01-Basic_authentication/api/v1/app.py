#!/usr/bin/env python3
"""API module for Flask app with authentication management."""

from flask import Flask, jsonify, abort, request
from flask_cors import CORS
from os import getenv

# Import the appropriate authentication classes
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth

app = Flask(__name__)
CORS(app)

# Initialize authentication variable
auth = None

# Load authentication type from environment variable
AUTH_TYPE = getenv("AUTH_TYPE")

if AUTH_TYPE == "basic_auth":
    auth = BasicAuth()
else:
    auth = Auth()

# Define routes
@app.route('/api/v1/status/', methods=['GET'])
def status():
    """Check the status of the API."""
    return jsonify({"status": "OK"})

@app.route('/api/v1/unauthorized/', methods=['GET'])
def unauthorized():
    """Test unauthorized access."""
    abort(401)

@app.route('/api/v1/forbidden/', methods=['GET'])
def forbidden():
    """Test forbidden access."""
    abort(403)

# Method to handle requests before routing them
@app.before_request
def before_request():
    """Filter requests before routing based on authentication."""
    if auth is None:
        return
    # List of paths that do not require authentication
    excluded_paths = ['/api/v1/status/', '/api/v1/unauthorized/', '/api/v1/forbidden/']
    # Check if the request path requires authentication
    if not auth.require_auth(request.path, excluded_paths):
        return
    # Check for the Authorization header; if not present, abort with a 401 error
    if auth.authorization_header(request) is None:
        abort(401)
    # Check for the current user; if not found, abort with a 403 error
    if auth.current_user(request) is None:
        abort(403)

# Error handlers for specific HTTP status codes
@app.errorhandler(401)
def unauthorized_error(error):
    """Handle 401 Unauthorized error."""
    return jsonify({"error": "Unauthorized"}), 401

@app.errorhandler(403)
def forbidden_error(error):
    """Handle 403 Forbidden error."""
    return jsonify({"error": "Forbidden"}), 403

# Start the Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

