#!/usr/bin/en python3
""" expects one string argument name password and returns a salted, hashed 
    password, which is a byte string
"""
from bcrypt import hashpw, salt


def hash_password(password: str) -> bytes:
    """Use the bcrypt package to perform the hashing (with hashpw)."""
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    if bcrypt.checkpw(password, hashed):
        return hashed
