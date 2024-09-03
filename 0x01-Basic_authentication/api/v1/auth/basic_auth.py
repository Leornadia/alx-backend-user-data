#!/usr/bin/env python3
"""
Module for Basic Authentication
"""

from api.v1.auth.auth import Auth
from models.user import User
import base64
from typing import TypeVar


class BasicAuth(Auth):
    """Basic Auth class that inherits from Auth"""

    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """
        Extracts the Base64 part of the Authorization header for Basic Authentication.

        Args:
            authorization_header (str): The Authorization header string.

        Returns:
            str: The Base64 part of the header or None if invalid.
        """
        if authorization_header is None or not isinstance(authorization_header, str):
            return None

        if not authorization_header.startswith("Basic "):
            return None

        # Return the part after "Basic " (which is index 6 onward)
        return authorization_header[6:]

    def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:
        """
        Decodes the Base64 Authorization header to a UTF-8 string.

        Args:
            base64_authorization_header (str): The Base64 encoded authorization header.

        Returns:
            str: The decoded value or None if the input is invalid.
        """
        if base64_authorization_header is None or not isinstance(base64_authorization_header, str):
            return None

        try:
            # Decode the Base64 string to bytes
            decoded_bytes = base64.b64decode(base64_authorization_header)
            # Convert bytes to string
            return decoded_bytes.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> (str, str):
        """
        Extracts the user email and password from the Base64 decoded value.

        Args:
            decoded_base64_authorization_header (str): Decoded Base64 authorization header.

        Returns:
            tuple: The user email and password, or (None, None) if invalid.
        """
        if decoded_base64_authorization_header is None or not isinstance(decoded_base64_authorization_header, str):
            return None, None

        if ':' not in decoded_base64_authorization_header:
            return None, None

        # Split the string into two parts using the first ':' as the separator
        email, password = decoded_base64_authorization_header.split(':', 1)
        return email, password

    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """
        Returns the User instance based on the user's email and password.

        Args:
            user_email (str): The user's email address.
            user_pwd (str): The user's password.

        Returns:
            User: The User instance, or None if invalid credentials.
        """
        if user_email is None or not isinstance(user_email, str):
            return None

        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        # Search for the user in the database by email
        users = User.search({'email': user_email})
        if not users:
            return None

        # Check if the password is valid
        user = users[0]
        if not user.is_valid_password(user_pwd):
            return None

        return user

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the User instance for a request.

        Args:
            request: The request object containing the Authorization header.

        Returns:
            User: The User instance or None if invalid.
        """
        auth_header = self.authorization_header(request)
        if not auth_header:
            return None

        base64_auth_header = self.extract_base64_authorization_header(auth_header)
        if not base64_auth_header:
            return None

        decoded_auth_header = self.decode_base64_authorization_header(base64_auth_header)
        if not decoded_auth_header:
            return None

        user_email, user_pwd = self.extract_user_credentials(decoded_auth_header)
        if not user_email or not user_pwd:
            return None

        return self.user_object_from_credentials(user_email, user_pwd)

