#!/usr/bin/env python3
"""
Session Authentication class
"""
from api.v1.auth.auth import Auth
import uuid
from typing import Union, Any
from models.user import User

class SessionAuth(Auth):
    """
    Session Authentication class that inherits from Auth
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Creates a Session ID for a user_id.

        Args:
            user_id (str): The user ID.

        Returns:
            str: The Session ID if successful, otherwise None.
        """
        if user_id is None or not isinstance(user_id, str):
            return None

        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> Union[str, None]:
        """
        Returns a User ID based on a Session ID.

        Args:
            session_id (str): The Session ID.

        Returns:
            str: The User ID if found, otherwise None.
        """
        if session_id is None or not isinstance(session_id, str):
            return None

        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request: Union[Any, None] = None) -> Union[User, None]:
        """
        Returns a User instance based on a cookie value.

        Args:
            request (flask.Request): The request object.

        Returns:
            User: The User instance if found, otherwise None.
        """
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return None
        return User.get(user_id)
