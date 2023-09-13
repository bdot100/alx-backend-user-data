#!/usr/bin/env python3
"""method that takes in a password string arguments
    and returns bytes
"""
import bcrypt


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
