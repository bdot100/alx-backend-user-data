#!/usr/bin/env python3
"""
This class will manage the API authentication.
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """Class to manage the api authentication"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Returns: False"""
        return False


    def authorization_header(self, request=None) -> str:
        """Returns: None"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Returns: None"""
        return None