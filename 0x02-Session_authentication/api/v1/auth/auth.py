#!/usr/bin/env python3
"""
Managing the API authentication
"""
from flask import request
from typing import List, TypeVar
import os


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
            bool
        """
        if not path or not excluded_paths or not len(excluded_paths):
            return True
        if path in excluded_paths or path + '/' in excluded_paths:
            return False
        if any(path.startswith(p[:-1]) for p in excluded_paths
               if p.endswith('*')):
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """
        This function will be used to retrieve the authorization key from
        the header of the request

        Attributes:
            request: Flask request object

        Returns:
            None
        """
        if not request or not request.headers.get("Authorization"):
            return None
        return request.headers.get("Authorization")

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

    def session_cookie(self, request=None):
        """
        This method returns the cookie value from a request as session
        id will be stored in a cookie when using the classic session
        authentiation

        Attributes:
        request

        Returns:
            the cookie value from a request
        """
        if not request:
            return None
        cookie_name = os.getenv('SESSION_NAME', "_my_session_id")
        return request.cookies.get(cookie_name)
