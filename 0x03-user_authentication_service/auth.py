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


def _generate_uuid() -> str:
    """return a string representation of a new UUID"""
    return str(uuid4())


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

    def valid_login(self, email: str, password: str) -> bool:
        """Validates login, if the user are valid or not"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        else:
            return bcrypt.checkpwd(password=password.encode('utf-8'),
                                   _hash_password=user.hashed_password)

    def create_session(self, email: str) -> str:
        """takes an email string argument and returns the string session ID"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return NoResultFound
        else:
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id

    def get_user_from_session_id(self, session_id: str) -> str:
        """returns the corresponding User or None"""
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        else:
            return user

    def destroy_session(self, user_id: int) -> None:
        """updates the corresponding user session ID to None"""
        try:
            self._db.update_user(user_id, session_id=None)
        except NoResultFound:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """Find the user corresponding to the email. If the user does not
        exist, raise a ValueError exception. If it exists, generate a UUID
        and update the user reset_token database field. Return the token"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError
        token = _generate_uuid()
        self._db.update_user(user.id, reset_token=token)
        return token

    def update_password(self, reset_token: str, password: str) -> None:
        """Use the reset_token to find the corresponding user. If it does not
        exist, raise a ValueError exception. Otherwise, hash the password and
        update the user hashed_password field with the new hashed password and
        the reset_token field to None"""
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError
        pwd = _hash_password(password)
        self._db.update_user(user, hashed_password=pwd, reset_token=None)
