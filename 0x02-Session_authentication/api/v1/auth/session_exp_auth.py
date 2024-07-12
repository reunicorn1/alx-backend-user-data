#!/usr/bin/env python3
"""
Class SessionExpAuth
"""
from api.v1.auth.session_auth import SessionAuth
import os
from datetime import datetime, timedelta
from models.user import User


class SessionExpAuth(SessionAuth):
    """
    This class defines session instances with an expiration date
    """
    def __init__(self):
        """
        The constructor of the SessionExpAuth
        """
        self.session_duration = os.getenv('SESSION_DURATION')
        self.session_duration = int(self.session_duration) if (
                self.session_duration and
                self.session_duration.isdigit()) else 0

    def create_session(self, user_id=None):
        """
        This overrrides the original create_session
        """
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        self.user_id_by_session_id[session_id] = {
                'user_id': user_id,
                'created_at': datetime.now()
                }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        This method overrrides the original user_id_for_session_id
        """
        if (not session_id or
                session_id not in self.user_id_by_session_id.keys()):
            return None
        if self.session_duration <= 0:
            return self.user_id_by_session_id[session_id]

        if (not self.user_id_by_session_id[session_id].get('created_at') or
                self.user_id_by_session_id[session_id]['created_at'] +
                timedelta(seconds=self.session_duration) < datetime.now()):
            return None
        return self.user_id_by_session_id[session_id]

    def current_user(self, request=None):
        """
        This method returns the current user instances out of the
        request during session authentication

        Attributes:
        request: flask request object

        Returns:
            user instance
        """
        dictionary = self.user_id_for_session_id(self.session_cookie(request))
        if dictionary:
            return User.get(dictionary['user_id'])
        return None
