#!/usr/bin/env python3
"""
Managing the API authentication
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """
    This class manages the API authentiation of users trying to access
    the api server

    Methods:
        require_auth
        authorization_header
        current_user
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        This function specifies certain endpoints of the api which require
        authentiation

        Attributes:
            path: str
            excluded_paths: list[str]

        Returns:
            False
        """
        return False

    def authorization_header(self, request=None) -> str:
        """
        This function will be used to retrieve the authorization key from
        the header of the request

        Attributes:
            request: Flask request object

        Returns:
            None
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        This function will be used the current user based on his
        authorization credentials

        Attributes:
            request: Flask request object

        Returns:
            None
        """
        return None
