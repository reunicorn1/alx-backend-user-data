#!/usr/bin/env python3
"""
Basic Authentication
"""
from api.v1.auth.auth import Auth
from models.user import User
from typing import TypeVar
import base64
import binascii


class BasicAuth(Auth):
    """
    This class inherits from Auth and applies the technique of
    Basic Authentication to authorize the credentials of a user
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
        This method returns the Base64 part of the authorization header
        for a Basic Authentication

        Parameters:
        authorization_header: str
            the string representation of the encoded auth token

        Returns:
            the ASCII decoded string of the token
        """
        if (not authorization_header or
                not isinstance(authorization_header, str) or
                not authorization_header.startswith('Basic ')):
            return None
        return authorization_header[len('Basic '):]

    def decode_base64_authorization_header(self, base64_authorization_header:
                                           str) -> str:
        """
        This method returns the decoded value of a Base64 string

        Parameters:
        base64_authorization_header: str
            the base64 part of the authorization header

        Returns:
            the decoded value of a Base64 string
        """
        if (not base64_authorization_header or
                not isinstance(base64_authorization_header, str)):
            return None
        try:
            d = base64.b64decode(base64_authorization_header).decode('utf-8')
        except binascii.Error:
            return None
        return d

    def extract_user_credentials(self, decoded_base64_authorization_header:
                                 str) -> (str, str):
        """
        This method returns the user email and password from the Base64
        decoded value

        Parameters:
        decoded_base64_authorization_header: str
            the string of username, password which is the decoded token

        Returns:
            A tuple of the user email and password
        """
        if (not decoded_base64_authorization_header or
                not isinstance(decoded_base64_authorization_header, str) or
                ':' not in decoded_base64_authorization_header):
            return None, None
        email, password = decoded_base64_authorization_header.split(':', 1)
        return email, password

    def user_object_from_credentials(self, user_email: str, user_pwd:
                                     str) -> TypeVar('User'):
        """
        This method returns a User instance based on his email and
        password

        Parameters:
        user_email: str
        user_pwd: str

        Returns:
            The user instance based on his credentials
        """
        if (not user_email or
                not isinstance(user_email, str) or
                not user_pwd or
                not isinstance(user_pwd, str)):
            return None
        try:
            users = User.search({"email": user_email})
            if not len(users) or not users[0].is_valid_password(user_pwd):
                return None
            return users[0]
        except KeyError:
            return None
