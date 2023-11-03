#!/usr/bin/en python3
""" expects one string argument name password and returns a salted, hashed 
    password, which is a byte string
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """Use the bcrypt package to perform the hashing (with hashpw)."""
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """validate hashed vs provided password"""
    password = password.encode("utf-8")
    return True if bcrypt.checkpw(password, hashed_password) else False
