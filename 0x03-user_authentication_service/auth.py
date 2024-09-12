#!/usr/bin/env python3
"""Auth module for user authentication.
"""

from db import DB
from user import User  # Make sure to import the User model
import bcrypt
from sqlalchemy.exc import NoResultFound


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def _hash_password(self, password: str) -> str:
        """
        Hash a password using bcrypt.

        Args:
            password (str): The password to hash.

        Returns:
            str: The hashed password.
        """
        # Hash the password using bcrypt and return the hashed value as a string
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def register_user(self, email: str, password: str) -> User:
        """
        Register a new user if it does not exist.

        Args:
            email (str): The email of the user.
            password (str): The password of the user.

        Returns:
            User: The newly created User object.

        Raises:
            ValueError: If a user with the given email already exists.
        """
        try:
            # Try to find a user with the given email
            user = self._db.find_user_by(email=email)
            # If user is found, raise a ValueError
            raise ValueError(f"User {email} already exists.")
        except NoResultFound:
            # If no user is found, proceed with registration
            hashed_password = self._hash_password(password)
            # Add the new user to the database
            new_user = self._db.add_user(email, hashed_password)
            return new_user

