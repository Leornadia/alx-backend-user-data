#!/usr/bin/env python3
"""Flask app for user registration."""
from flask import Flask, request, jsonify
from auth import Auth

# Instantiate the Auth object
AUTH = Auth()

# Create an instance of the Flask class
app = Flask(__name__)

@app.route("/", methods=["GET"])
def welcome():
    """Root endpoint that returns a welcome message."""
    return jsonify({"message": "Bienvenue"})

@app.route("/users", methods=["POST"])
def users():
    """
    Register a new user.
    
    Expects 'email' and 'password' form data.
    
    Returns:
        Response: JSON payload with user registration status.
    """
    # Get the email and password from the form data
    email = request.form.get("email")
    password = request.form.get("password")

    try:
        # Try to register the user
        user = AUTH.register_user(email, password)
        # If successful, return a JSON response
        return jsonify({"email": user.email, "message": "user created"}), 200
    except ValueError:
        # If the user is already registered, return an error message
        return jsonify({"message": "email already registered"}), 400

# Run the Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

