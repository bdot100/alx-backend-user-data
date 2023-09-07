#!/usr/bin/env python3
"""
This class will manage the API authentication through
session auth.
"""
import uuid
from api.v1.auth.auth import Auth


class SessionAuth(Auth):
    """
    Session authentication class
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        This Function Creates a Session ID for a user_id.

        Args:
            user_id (str): The user ID to create a session for.

        Returns:
            str: The created Session ID.
        """
        if user_id is None or not isinstance(user_id, str):
            return None

        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        This Function Returns a User ID based on a Session ID.

        Args:
            session_id (str): The Session ID to retrieve the User ID for.

        Returns:
            str: The User ID associated with the Session ID,
            or None if not found.
        """
        if session_id is None or not isinstance(session_id, str):
            return None

        return self.user_id_by_session_id.get(session_id)
