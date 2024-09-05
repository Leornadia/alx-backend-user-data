#!/usr/bin/env python3
"""
Module for the Users endpoints.
"""
from flask import jsonify, abort
from api.v1.views import app_views
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """
    Retrieves all users.
    """
    all_users = User.all()
    return jsonify([user.to_json() for user in all_users])


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """
    Retrieves a user by ID.
    """
    user = User.get(user_id)
    if user is None:
        abort(404)
    if user_id == "me" and request.current_user is None:
        abort(404)
    if user_id == "me" and request.current_user is not None:
        return jsonify(request.current_user.to_json())
    return jsonify(user.to_json())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """
    Deletes a user by ID.
    """
    user = User.get(user_id)
    if user is None:
        abort(404)
    user.delete()
    return jsonify({}), 204


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """
    Creates a new user.
    """
    req = request.get_json()
    if not req:
        abort(400, description="Not a JSON")
    if 'email' not in req or 'password' not in req:
        abort(400, description="Missing email or password")
    user = User()
    user.email = req.get('email')
    user.password = req.get('password')
    if not user.save():
        abort(500)
    return jsonify(user.to_json()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """
    Updates a user by ID.
    """
    user = User.get(user_id)
    if user is None:
        abort(404)
    req = request.get_json()
    if not req:
        abort(400, description="Not a JSON")
    for key, value in req.items():
        setattr(user, key, value)
    if not user.save():
        abort(500)
    return jsonify(user.to_json()), 200
