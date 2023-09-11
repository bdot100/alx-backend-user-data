#!/usr/bin/env python3
"""
This class will manage the API authentication through
session auth.
"""
import uuid
from api.v1.auth.auth import Auth
from models.user import User


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

    def current_user(self, request=None):
        """
        This Function  (overload) that returns a User instance
        based on a cookie value

        Args:
            request : request object containing cookie

        Returns:
            The user instance, if the cookie does not exists,
            returns None
        """
        if request is None:
            return None

        session_cookie = self.session_cookie(request)
        if session_cookie is None:
            return None

        user_id = self.user_id_for_session_id(session_cookie)
        if user_id is None:
            return None

        # Retrieve the User instance from the database based on user_id
        user = User.get(user_id)
        return user

    def destroy_session(self, request=None):
        """
        This Function deletes the user session/logout

        Args:
            request : flask request object

        Returns:
        """
        if request is None:
            return False

        # Get the Session ID from the request's cookie
        session_id = self.session_cookie(request)

        # If there's no Session ID cookie, return False
        if session_id is None:
            return False

        # Get the User ID associated with the Session ID
        user_id = self.user_id_for_session_id(session_id)

        # If the Session ID is not linked to any User ID, return False
        if user_id is None:
            return False

        # Delete the Session ID from the dictionary
        del self.user_id_by_session_id[session_id]
        return True
