#!/usr/bin/env python3

"""DB module.
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance.
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Adds a new user to the database
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()

        return user

    def find_user_by(self, **kwargs) -> User:
        """Finds a user based on keyworded attributes
        """
        for k in kwargs:
            if not hasattr(User, k):
                raise InvalidRequestError
        result = self._session.query(User).filter_by(**kwargs).first()
        if not result:
            raise NoResultFound
        return result

    def update_user(self, user_id: int, **kwargs) -> None:
        """Finds a user and then updates his attributes
        """
        try:
            user = self.find_user_by(id=user_id)
        except InvalidRequestError or NoResultFound:
            return

        attrs = {"id": int, "email": str, "hashed_password": str,
                 "session_id": str, "reset_token": str}
        for k, v in kwargs.items():
            if hasattr(User, k) and attrs[k] == type(v):
                setattr(user, k, v)
            else:
                raise ValueError

        self._session.commit()
