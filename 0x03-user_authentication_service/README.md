0x03. User authentication service
Description
This project implements a basic user authentication service using Flask and SQLAlchemy. It covers the essential functionalities of registration, login, and logout, providing a foundation for building more complex authentication systems.
Requirements
Python 3.7
Flask
SQLAlchemy 1.3.x
Requests module
SQLite3 (for database)
Project Structure
auth_service/
├── app.py
├── auth.py
├── db.py
├── __init__.py
└── models.py

File Breakdown
app.py
#!/usr/bin/env python3
"""
This is the main Flask application file. It handles routing,
sets up the database, and manages user interactions with the
authentication service.
"""

from flask import Flask, request, jsonify, redirect, url_for, session
from flask_cors import CORS

from .auth import Auth
from .db import DB

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with a secure secret key
CORS(app)

db = DB()
auth = Auth(db)

@app.route('/register', methods=['POST'])
def register():
    """
    Registers a new user.
    """
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid request'}), 400
    try:
        user = auth.register_user(data['username'], data['password'])
        return jsonify({'message': 'User registered successfully', 'user_id': user.id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/login', methods=['POST'])
def login():
    """
    Logs in an existing user.
    """
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid request'}), 400
    try:
        user = auth.login_user(data['username'], data['password'])
        session['user_id'] = user.id
        return jsonify({'message': 'Login successful'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 401

@app.route('/logout', methods=['GET'])
def logout():
    """
    Logs out the current user.
    """
    if 'user_id' in session:
        session.pop('user_id')
        return jsonify({'message': 'Logout successful'}), 200
    return jsonify({'error': 'Not logged in'}), 401

@app.route('/protected', methods=['GET'])
def protected():
    """
    Protected route accessible only to authenticated users.
    """
    if 'user_id' in session:
        user_id = session['user_id']
        user = db.get_user(user_id)
        return jsonify({'message': f'Welcome, {user.username}!'}), 200
    return jsonify({'error': 'Unauthorized'}), 401

if __name__ == '__main__':
    app.run(debug=True)

auth.py
#!/usr/bin/env python3
"""
This module handles user authentication logic.
"""

from werkzeug.security import generate_password_hash, check_password_hash

class Auth:
    """
    The Auth class manages user authentication operations.
    """

    def __init__(self, db):
        self.db = db

    def register_user(self, username, password):
        """
        Registers a new user.
        """
        if self.db.get_user(username):
            raise ValueError('Username already exists')
        hashed_password = generate_password_hash(password)
        user = self.db.create_user(username, hashed_password)
        return user

    def login_user(self, username, password):
        """
        Logs in an existing user.
        """
        user = self.db.get_user(username)
        if not user:
            raise ValueError('Invalid username or password')
        if not check_password_hash(user.password, password):
            raise ValueError('Invalid username or password')
        return user

db.py
#!/usr/bin/env python3
"""
This module manages database interactions.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from .models import User

Base = declarative_base()

class DB:
    """
    The DB class handles database operations.
    """

    def __init__(self):
        engine = create_engine('sqlite:///auth.db')
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def create_user(self, username, password):
        """
        Creates a new user in the database.
        """
        user = User(username=username, password=password)
        self.session.add(user)
        self.session.commit()
        return user

    def get_user(self, username_or_id):
        """
        Retrieves a user from the database by username or ID.
        """
        if isinstance(username_or_id, int):
            return self.session.query(User).filter_by(id=username_or_id).first()
        else:
            return self.session.query(User).filter_by(username=username_or_id).first()

models.py
#!/usr/bin/env python3
"""
This module defines the database models.
"""

from sqlalchemy import Column, Integer, String
from .db import Base

class User(Base):
    """
    The User model represents a user in the database.
    """

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

init.py
#!/usr/bin/env python3
"""
This file serves as an empty initialization file.
"""

Running the Application
Install the required packages:
pip install flask sqlalchemy requests flask-cors

Run the app:
python app.py

Access the API endpoints using a web browser or REST client.
Example Usage
Registering a new user:
curl -X POST -H "Content-Type: application/json" -d '{"username": "john.doe", "password": "password123"}' http://127.0.0.1:5000/register

Logging in:
curl -X POST -H "Content-Type: application/json" -d '{"username": "john.doe", "password": "password123"}' http://127.0.0.1:5000/login

Accessing a protected route:
curl -H "Cookie: session=your_session_cookie" http://127.0.0.1:5000/protected
