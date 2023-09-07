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
    pass
