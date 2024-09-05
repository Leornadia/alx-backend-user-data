#!/usr/bin/env python3
"""Auth module for API authentication management."""

from flask import request
from typing import List, TypeVar
import os

class Auth:
    """Class to manage the API authentication."""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determines if authentication is required for a given path.

        Args:
            path (str): The request path.
            excluded_paths (List[str]): A list of paths that do not require authentication.

        Returns:
            bool: True if the path requires authentication, False otherwise.
        """
        if path is None:
            return True
        if not excluded_paths:
            return True

        # Normalize path by ensuring it ends with a '/'
        if path[-1] != '/':
            path += '/'

        # Check if the normalized path is in the excluded paths
        for excluded_path in excluded_paths:
            # Handle wildcard pattern in excluded paths
            if excluded_path.endswith('*'):
                if path.startswith(excluded_path[:-1]):
                    return False
            else:
                if path == excluded_path or path.rstrip('/') == excluded_path.rstrip('/'):
                    return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Returns the value of the Authorization header from a Flask request object.

        Args:
            request (Flask.request): The Flask request object.

        Returns:
            str: The value of the Authorization header, or None if not present.
        """
        if request is None:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Returns the current user from the request, if available.

        Args:
            request (Flask.request): The Flask request object.

        Returns:
            TypeVar('User'): None for now. To be implemented later.
        """
        return None

    def session_cookie(self, request=None):
        """
        Returns a cookie value from a request, specifically the session cookie.

        Args:
            request (Flask.request): The Flask request object.

        Returns:
            str or None: The value of the session cookie, or None if not found.
        """
        if request is None:
            return None

        # Get the session name from the environment variable SESSION_NAME
        session_name = os.getenv('SESSION_NAME')

        # Return the value of the cookie with the name stored in session_name
        return request.cookies.get(session_name)

