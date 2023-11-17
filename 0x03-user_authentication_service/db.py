#!/usr/bin/env python3
"""DB module"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from user import Base, User

from user import Base


class DB:
    """DB class"""

    def __init__(self) -> None:
        """Initialize a new DB instance"""
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object"""
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """save the user to the database and return User object"""
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """takes in arbitrary keyword arguments and returns the first row
        found in the users table as filtered by the method input arguments
        """
        if kwargs is None:
            raise InvalidRequestError
        user = self._session.query(User).filterBy(**kwargs).first
        if user is None:
            raise NoResultFound
        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """takes as argument a required user_id integer and arbitrary keyword
        arguments, and returns None
        update the user attributes as passed in the method’s arguments
        then commit changes to the database"""
        u_id = self.find_user_by(id=user_id)
        for key, value in kwargs.items():
            if not hasattr(u_id, key):
                raise ValueError
            setattr(u_id, key, value)
        self._session.commit()
