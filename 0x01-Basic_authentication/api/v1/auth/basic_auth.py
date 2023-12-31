#!/usr/bin/env python3
"""Basic class that inherits from Auth"""
from api.v1.auth.auth import Auth
from base64 import b64decode
from typing import TypeVar
from models.user import User
import base64


class BasicAuth(Auth):
    """An empty class"""
    pass

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """returns the Base64 part of the Authorization header for
            a Basic Authentication
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        base = authorization_header.split(' ')
        return base[1]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """returns the decoded value of a Base64 string """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None

        try:
            decoded_value = base64.b64decode(
                base64_authorization_header).decode('utf-8')
            return decoded_value
        except Exception as e:
            """ Handle decoding error"""
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """Extract user email and password from the decoded Base64-encoded
        authorization header.
        :param decoded_base64_authorization_header: Decoded Base64-encoded
        authorization header
        :type decoded_base64_authorization_header: str
        :return: Tuple containing user email and user password or (None, None)
        if extraction fails
        :rtype: tuple
        """
        if (decoded_base64_authorization_header is None
            or not isinstance(decoded_base64_authorization_header, str
                              ) or ':'
                              not in decoded_base64_authorization_header):
            return None, None

        """
        # Split the decoded value into email and password using the colon(:)
        """
        user_email, user_password = decoded_base64_authorization_header.split(
            ':', 1)
        return user_email, user_password
    
    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """
        Get the User instance based on user email and password.

        :param user_email: User email
        :type user_email: str
        :param user_pwd: User password
        :type user_pwd: str
        :return: User instance or None if not found or invalid credentials
        :rtype: TypeVar('User')
        """
        if user_email is None or not isinstance(user_email, str) or user_pwd is None or not isinstance(user_pwd, str):
            return None

        # Search for the user in the database (file) based on email
        users = User.search({'email': user_email})

        if not users:
            # No user found with the given email
            return None

        # Assume the first user in the list is the one we're looking for
        found_user = users[0]

        # Check if the provided password is valid for the found user
        if not found_user.is_valid_password(user_pwd):
            return None

        return found_user
