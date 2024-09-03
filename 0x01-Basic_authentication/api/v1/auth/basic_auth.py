#!/usr/bin/env python3
"""
Module for Basic Authentication
"""

from api.v1.auth.auth import Auth


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

