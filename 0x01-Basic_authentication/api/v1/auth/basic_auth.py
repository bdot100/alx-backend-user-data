#!/usr/bin/env python3
"""
This class will manage the API authentication through
basic auth.
"""
from flask import request
from typing import List, TypeVar
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """Class to manage the api authentication
        through basic auth.
    """

    def extract_base64_authorization_header(self, authorization_header: str)\
            -> str:
        """
        This Function Extracts the Base64 part of the Authorization header
        for Basic Authentication.

        Args:
            authorization_header (str): The Authorization header.

        Returns:
            str: The Base64 part of the Authorization header.
        """
        if (
            authorization_header is None
            or not isinstance(authorization_header, str)
            or not authorization_header.startswith("Basic ")
        ):
            return None
        return authorization_header.split(" ")[-1]
