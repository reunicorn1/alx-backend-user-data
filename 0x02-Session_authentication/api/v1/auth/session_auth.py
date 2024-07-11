#!/usr/bin/env python3
"""
Session Auth Object
"""
from api.v1.auth.auth import Auth
from models.user import User
import uuid


class SessionAuth(Auth):
    """
    This class is the session object which represent how the user
    authenticate his access to the server to get authorized to access
    resources available

    Methods:
        create_session
        user_id_for_session_id
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        This method creates a session_id for a user_id

        Attributes:
        user_id: str

        Returns:
            the session id
        """
        if not user_id or not isinstance(user_id, str):
            return None
        _id = str(uuid.uuid4())
        self.user_id_by_session_id[_id] = user_id
        return _id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        This method returns the user instance based on the session_id

        Attributes:
        session_id: str

        Returns:
            the user instance' id
        """
        if not session_id or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """
        This method returns the current user instances out of the
        request during session authentication

        Attributes:
        request: flask request object

        Returns:
            user instance
        """
        user_id = self.user_id_for_session_id(self.session_cookie(request))
        if user_id:
            return User.get(user_id)
        return None

    def destroy_session(self, request=None):
        """
        This method deletes the user session and logs him out

        Attributes:
        request: flask request object

        Returns:
            a boolean of the success of the procedure
        """
        if not request or not self.session_cookie(request):
            return False
        session_id = self.session_cookie(request)
        if not self.user_id_for_session_id(session_id):
            return False
        self.user_id_by_session_id.pop(session_id)
        return True
