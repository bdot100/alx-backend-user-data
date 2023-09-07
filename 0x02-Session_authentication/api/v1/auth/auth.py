#!/usr/bin/env python3
"""
This class will manage the API authentication.
"""
from flask import request
from typing import List, TypeVar
import os


class Auth:
    """Class to manage the api authentication"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Method that returns True if the path is not in the list of strings
        excluded_paths:

        - Returns True if path is None
        - Returns True if excluded_paths is None or empty
        - Returns False if path is in excluded_paths

        You can assume excluded_paths contains string path always ending by a /
        This method must be slash tolerant: path=/api/v1/status and
        path=/api/v1/status/ must be returned False if excluded_paths contains
        /api/v1/status/
        """
        if path is None:
            return True
        elif excluded_paths is None or not excluded_paths:
            return True
        elif path in excluded_paths:
            return False
        else:
            for p in excluded_paths:
                if p.startswith(path):
                    return False
                if path.startswith(p):
                    return False
                if p[-1] == "*":
                    if path.startswith(p[:-1]):
                        return False
        return True

    def authorization_header(self, request=None) -> str:
        """
        This Method that returns the value of the
        Authorization header in a Flask
        request.

        Args:
            request (flask.Request): The Flask request
            object.

        Returns:
            str: The value of the Authorization header,
            or None if it doesn't
            exist.
        """
        if request is None:
            return None

        auth_header = request.headers.get('Authorization')
        if auth_header is None:
            return None
        return auth_header

    def current_user(self, request=None) -> TypeVar('User'):
        """Returns: None"""
        return None

    def session_cookie(self, request=None) -> str:
        """
        This Function Returns a cookie value from a request.

        Args:
            request (Request): The Flask request object.

        Returns:
            str: The value of the session cookie, or None if not found.
        """
        if request is None:
            return None

        session_name = os.getenv('SESSION_NAME')
        return request.cookies.get(session_name)
