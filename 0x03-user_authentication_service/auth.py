#!/usr/bin/env python3
"""Has password"""
from user import User
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4
import bcrypt


def _hash_password(password: str) -> bytes:
    """takes in a password string arguments and returns salted hash bytes"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self) -> None:
        """Constructor method for the class"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """creates a user based on the parameters supplied and
        return the User object"""
        try:
            user = self.db.find_user_by(email)
        except NoResultFound:
            pwd = _hash_password(password)
            user = self._db.add_user(email, pwd)
            return user
        else:
            raise ValueError('User {email} already exists')
