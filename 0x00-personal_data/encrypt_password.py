#!/usr/bin/en python3
""" expects one string argument name password and returns a salted, hashed 
    password, which is a byte string
"""


def hash_password(password: str) -> bytes:
    """Use the bcrypt package to perform the hashing (with hashpw)."""
    from bcrypt import hashpw, gensalt

    password, salt = bytes(password.encode()), gensalt()
    return hashpw(password, salt)
