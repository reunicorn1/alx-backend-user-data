#!/usr/bin/env python3
"""
Authentication class
"""
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

    @property
    def _generate_uuid() -> str:
        """This method generate random uuids
        """
        return str(uuid.uuid4())
