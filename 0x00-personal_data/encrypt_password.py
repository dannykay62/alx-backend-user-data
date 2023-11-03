#!/usr/bin/en python3
""" expects one string argument name password and returns a salted, hashed 
    password, which is a byte string
"""
from bcrypt import hashpw, gensalt


def hash_password(password: str) -> bytes:
    """Use the bcrypt package to perform the hashing (with hashpw)."""
    password, salt = bytes(password.encode()), gensalt()
    return hashpw(password, gensalt)
