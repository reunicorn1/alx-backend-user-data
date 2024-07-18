#!/usr/bin/env python3
"""
Authentication class
"""
from typing import Optional
import bcrypt
from sqlalchemy.orm.exc import NoResultFound
from user import User
from db import DB
import uuid


def _hash_password(password: str) -> bytes:
    """Hashing passwords and convertin them to bytes
    """
    bytes = password.encode('utf-8')
    return bcrypt.hashpw(bytes, bcrypt.gensalt())


def _generate_uuid() -> str:
    """This method generate random uuids
    """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Registers a user to the database
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists.")
        except NoResultFound:
            password = _hash_password(password)
            return self._db.add_user(email, password)

    def valid_login(self, email: str, password: str) -> bool:
        """This method validates login if the password matches
        what's already registerd
        """
        try:
            user = self._db.find_user_by(email=email)
            if bcrypt.checkpw(password.encode("utf-8"), user.hashed_password):
                return True
        except NoResultFound:
            pass
        return False

    def create_session(self, email: str) -> str:
        """This method creates a session id for every login of the user
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> Optional[User]:
        """This method returns a user based on the session_id provided
        """
        if session_id:
            try:
                user = self._db.find_user_by(session_id=session_id)
                return user
            except NoResultFound:
                return None

    def destroy_session(self, user_id) -> None:
        """This method destroys a session for an active user
        """
        if not user_id:
            return None
        self._db.update_user(user_id, session_id=None)
