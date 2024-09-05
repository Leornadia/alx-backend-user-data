#!/usr/bin/env python3
"""API module for Flask app with authentication management."""

from flask import Flask, jsonify, abort, request
from flask_cors import CORS
from os import getenv

# Import the appropriate authentication classes
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth
from api.v1.auth.session_auth import SessionAuth  # Import the session auth class

app = Flask(__name__)
CORS(app)

# Initialize authentication variable
auth = None

# Load authentication type from environment variable
AUTH_TYPE = getenv("AUTH_TYPE")

if AUTH_TYPE == "basic_auth":
    auth = BasicAuth()
elif AUTH_TYPE == "session_auth":  # Check if session authentication is chosen
    auth = SessionAuth()
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

# New route to return the authenticated user
@app.route('/api/v1/users/me', methods=['GET'])
def users_me():
    """Retrieve the authenticated User object."""
    if request.current_user is None:
        abort(404)  # User is not authenticated
    return jsonify(request.current_user.to_dict())  # Return the user info

# Method to handle requests before routing them
@app.before_request
def before_request():
    """Filter requests before routing based on authentication."""
    if auth is None:
        return
    # List of paths that do not require authentication
    excluded_paths = ['/api/v1/status/', '/api/v1/unauthorized/', '/api/v1/forbidden/', '/api/v1/auth_session/login/']
    # Check if the request path requires authentication
    if not auth.require_auth(request.path, excluded_paths):
        return
    # Check for the Authorization header or session cookie; if not present, abort with a 401 error
    if auth.authorization_header(request) is None and auth.session_cookie(request) is None:
        abort(401)
    # Check for the current user; if not found, abort with a 403 error
    request.current_user = auth.current_user(request)
    if request.current_user is None:
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

@app.errorhandler(404)
def not_found_error(error):
    """Handle 404 Not Found error."""
    return jsonify({"error": "Not found"}), 404

# Start the Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

