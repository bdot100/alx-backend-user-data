#!/usr/bin/env python3
"""
This class will manage the API authentication through
basic auth.
"""
import base64
from flask import request
from typing import List, TypeVar
from api.v1.auth.auth import Auth
from models.user import User


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

    def decode_base64_authorization_header(
        self, base64_authorization_header: str
    ) -> str:

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
            decoded = base64.b64decode(base64_authorization_header)\
                    .decode('utf-8')
            return decoded
        except Exception as e:
            return None

    def extract_user_credentials(
        self, decoded_base64_authorization_header: str
    ) -> (str, str):
        """
        This function extracts user credentials from a decoded
        Base64 authorization header.

        Args:
            decoded_base64_authorization_header (str): The
            decoded Base64 authorization header.

        Returns:
            tuple: A tuple containing the user email and password.

            Returns (None, None) if the input is None, not a string,
            or does not contain a ':'.

        Example:
            If decoded_base64_authorization_header is
            'user@example.com:password123',
            this method will return ('user@example.com',
            'password123').
        """
        if decoded_base64_authorization_header is None:
            return (None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        # if ':' not in decoded_base64_authorization_header:
        #     return (None, None)
        parts = decoded_base64_authorization_header.split(':', 1)
        if len(parts) < 2:
            return (None, None)

        email, password = parts[0], parts[1]
        # decoded_base64_authorization_header.split(':', 1)
        return (email, password)

    def user_object_from_credentials(
        self, user_email: str, user_pwd: str
    ) -> TypeVar('User'):
        """
        This Function Get a User instance based on email and
        password credentials.

        Args:
            user_email (str): The user's email.
            user_pwd (str): The user's password.

        Returns:
            User: The User instance if credentials are valid,
            else None.
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        try:
            # Use the User class's search method to look up users by email
            users = User.search({'email': user_email})
            # No user with the provided email found or user is empty
            if not users or users == []:
                return None
            # Check if the password is valid for any of the found users
            for user in users:
                if user.is_valid_password(user_pwd):
                    return user
            # No user with a matching password found
            return None
        except Exception:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        This function retrieves the User instance for a
        request using Basic Authentication.

        Args:
            request (Request): The Flask request object
            containing the Authorization header.

        Returns:
            User: The User instance if authentication is
            successful, else None.
        """
        if request is None:
            return None

        auth_header = self.authorization_header(request)

        if auth_header is None:
            return None

        base64_auth_header = self.extract_base64_authorization_header(
            auth_header
        )

        if base64_auth_header is None:
            return None

        decoded_auth_header = self.decode_base64_authorization_header(
            base64_auth_header
        )

        if decoded_auth_header is None:
            return None

        user_email, user_pwd = self.extract_user_credentials(
            decoded_auth_header
        )

        if user_email is None or user_pwd is None:
            return None

        return self.user_object_from_credentials(user_email, user_pwd)
