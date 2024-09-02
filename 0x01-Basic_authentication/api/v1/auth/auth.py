#!/usr/bin/env python3
""" Auth class python file """

from flask import request
from typing import List, TypeVar


class Auth:
    """Manages the API authentication"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Determines whether a given path requires authentication or not"""
        return False

    def authorization_header(self, request=None) -> str:
        '''returns None - request will be the Flask request object'''
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        '''request will be the Flask request object'''
        return None
