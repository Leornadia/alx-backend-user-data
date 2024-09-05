#!/usr/bin/env python3
""" Session Authentication views
"""
from flask import request, jsonify, abort
from models.user import User
from api.v1.views import app_views
import os

@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def auth_session_login():
    """ POST /auth_session/login
        Handles user login and session creation
    """
    # Retrieve email and password from form data
    email = request.form.get('email')
    password = request.form.get('password')

    # Check if email or password is missing
    if email is None or email == "":
        return jsonify({"error": "email missing"}), 400
    if password is None or password == "":
        return jsonify({"error": "password missing"}), 400

    # Search for the user by email
    try:
        users = User.search({"email": email})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404

    if not users or len(users) == 0:
        return jsonify({"error": "no user found for this email"}), 404

    user = users[0]

    # Check if password is valid
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    # Create a session for the user
    from api.v1.app import auth  # Import only where needed
    session_id = auth.create_session(user.id)

    # Get session name from environment variable
    session_name = os.getenv("SESSION_NAME")

    # Create response with user's info in JSON format
    response = jsonify(user.to_json())

    # Set cookie with the session ID
    response.set_cookie(session_name, session_id)

    return response

