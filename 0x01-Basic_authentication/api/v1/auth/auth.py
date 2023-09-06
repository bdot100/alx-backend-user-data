#!/usr/bin/env python3
"""
This class will manage the API authentication.
"""
from flask import request
from typing import List, TypeVar


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

        if excluded_paths is None or not excluded_paths:
            return True

        for p in excluded_paths:
            if p.endswith('/'):
                p = p[:-1]  # Remove the trailing slash

            if path == p or path.startswith(p + '/'):
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """Returns: None"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Returns: None"""
        return None
