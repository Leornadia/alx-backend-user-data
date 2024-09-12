#!/usr/bin/env python3
"""Auth module for user authentication and management."""
from db import DB
from user import User
import bcrypt
from sqlalchemy.orm.exc import NoResultFound


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Registers a new user if they don't exist."""
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            # If no user is found, register a new one
            hashed_password = self._hash_password(password)
            user = self._db.add_user(email, hashed_password)
            return user

    def _hash_password(self, password: str) -> bytes:
        """Hashes a password using bcrypt."""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validates user login credentials.
        
        Args:
            email (str): The email of the user.
            password (str): The password provided for authentication.
        
        Returns:
            bool: True if login is successful, False otherwise.
        """
        try:
            # Locate the user by email
            user = self._db.find_user_by(email=email)
            # Check if the provided password matches the stored hashed password
            if bcrypt.checkpw(password.encode('utf-8'), user.hashed_password):
                return True
            else:
                return False
        except NoResultFound:
            # If the user is not found, return False
            return False

