#!/usr/bin/env python3
"""method that takes in a password string arguments
    and returns bytes
"""
import bcrypt
from sqlalchemy.orm.exc import NoResultFound
import uuid
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


def _generate_uuid() -> str:
    """
    This Method Generate a new UUID and return it as a string.

    Returns:
        str: A string representation of the generated UUID.
    """
    return str(uuid.uuid4())


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

    def valid_login(self, email: str, password: str) -> bool:
        """
        This method Check if a user with the given email and
        password exists and is valid.

        Args:
            email (str): The user's email.
            password (str): The provided password.

        Returns:
            bool: True if the login is valid, False otherwise.
        """
        try:
            # Find the user by email
            user = self._db.find_user_by(email=email)

            # Compare the provided password with the stored hashed password
            return bcrypt.checkpw(
                password.encode('utf-8'), user.hashed_password)
        except NoResultFound:
            # If no user is found, return False
            return False

    def create_session(self, email: str) -> str:
        """
        This Method Creates a new session for the
        user with the given email.

        Args:
            email (str): The user's email.

        Returns:
            str: The generated session ID as a string.
        """
        try:
            # Find the user by email
            user = self._db.find_user_by(email=email)

            # Generate a new session ID
            session_id = _generate_uuid()

            # Update the user's session ID in the database
            self._db.update_user(user.id, session_id=session_id)

            # Return the generated session ID
            return session_id
        except NoResultFound:
            # If no user is found, raise an exception or return
            # an error message
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """
        This Method Gets the corresponding User based on a session ID.

        Args:
            session_id (str): The session ID to look up.

        Returns:
            User: The corresponding User if found, or None.
        """
        if session_id is None:
            return None

        try:
            # Find the user by session ID
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            # If no user is found, return None
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        This Method Set the session ID of the corresponding user to None.

        Args:
            user_id (int): The ID of the user for whom to destroy the session.
        """
        try:
            # Update the user's session ID to None
            self._db.update_user(user_id, session_id=None)
        except NoResultFound:
            # Handle the case where no user is found based on the user_id
            return None
        return None

    def get_reset_password_token(self, email: str) -> str:
        """
        This Method Generate a reset password token for the
        user with the given email.

        Args:
            email (str): The user's email.

        Returns:
            str: The generated reset password token.
        """
        try:
            # Find the user by email
            user = self._db.find_user_by(email=email)

            # Generate a new reset password token
            reset_token = _generate_uuid()

            # Update the user's reset_token field in the database
            self._db.update_user(user.id, reset_token=reset_token)

            # Return the generated reset password token
            return reset_token
        except NoResultFound:
            # If no user is found, raise a ValueError
            raise ValueError("User not found for the provided email")

    def update_password(self, reset_token: str, password: str) -> None:
        """
        This Method Update the user's password based on a reset token.

        Args:
            reset_token (str): The reset token used to locate the user.
            password (str): The new password to set for the user.
        """
        try:
            # Find the user by reset token
            user = self._db.find_user_by(reset_token=reset_token)

            # Hash the new password
            hashed_password = bcrypt.hashpw(
                password.encode('utf-8'),
                bcrypt.gensalt()
            )

            # Update the user's hashed_password field with the new
            # hashed password and the reset_token field to None
            self._db.update_user(
                user.id,
                hashed_password=hashed_password,
                reset_token=None
            )
        except NoResultFound:
            # If no user is found (based on reset token), raise a ValueError
            raise ValueError("Invalid reset token")
