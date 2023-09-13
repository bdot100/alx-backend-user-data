#!/usr/bin/env python3
"""method that takes in a password string arguments
    and returns bytes
"""
import bcrypt
from sqlalchemy.orm.exc import NoResultFound
from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """
    This Method Hashes the input password using
    bcrypt with a random salt.

    Args:
        password (str): The password to hash.

    Returns:
        bytes: The salted hash of the input password.
    """
    # Generate a random salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    return hashed_password


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        This Method Register a new user with the provided
        email and password.

        Args:
            email (str): The user's email.
            password (str): The user's password.

        Returns:
            User: The User object for the newly registered user.

        Raises:
            ValueError: If a user with the same email already exists.
        """
        try:
            # Check if a user with the provided email already exists
            existing_user = self._db.find_user_by(email=email)
        except NoResultFound:
            # Hash the password
            hashed_password = _hash_password(password)
            # Create a new User object and save it to the database
            new_user = self._db.add_user(email, hashed_password)
            return new_user
        raise ValueError(f"User {email} already exists")
