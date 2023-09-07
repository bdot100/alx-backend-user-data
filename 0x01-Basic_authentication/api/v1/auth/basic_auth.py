#!/usr/bin/env python3
"""
This class will manage the API authentication through
basic auth.
"""
import base64
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
    
    def decode_base64_authorization_header(self, base64_authorization_header: str)\
            -> str:
        """
        This Function Decodes the value of a Base64 string 
        base64_authorization_header.

        Args:
            base64_authorization_header (str): The Base64 authorization header.

        Returns:
            str: The decoded value as UTF8 string.
        """
        if (
            base64_authorization_header is None
            or not isinstance(base64_authorization_header, str)
        ):
            return None
        try:
            decoded = base64.b64decode(base64_authorization_header).decode('utf-8')
            return decoded
        except Exception as e:
            return None
