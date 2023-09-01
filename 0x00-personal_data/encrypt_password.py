#!/usr/bin/env python3
"""
This module defines functions for password hashing and validation.
"""

import bcrypt
from bcrypt import hashpw


def hash_user_password(password: str) -> bytes:
    """
    Hashes a user's password for secure storage.

    Args:
        password (str): The user's plaintext password.

    Returns:
        bytes: The hashed password.
    """
    password_bytes = password.encode()
    hashed_password = hashpw(password_bytes, bcrypt.gensalt())
    return hashed_password


def is_password_valid(hashed_password: bytes, candidate_password: str) -> bool:
    """
    Validates a candidate password against a stored hashed password.

    Args:
        hashed_password (bytes): The stored hashed password.
        candidate_password (str): The candidate password for validation.

    Returns:
        bool: True if the candidate password is valid, False otherwise.
    """
    candidate_bytes = candidate_password.encode()
    return bcrypt.checkpw(candidate_bytes, hashed_password)
