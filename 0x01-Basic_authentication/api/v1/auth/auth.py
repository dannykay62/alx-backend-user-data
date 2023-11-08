#!/usr/bin/env python3
"""Class Auth to manage the API authentication"""
from flask import requests
from typing import List, TypeVar


class Auth():
    """Manage the API authentication"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Check if authentication is required for a given path"""
        if path is None or excluded_paths is None or not len(excluded_paths):
            return True
        if path[-1] != '/':
            path += '/'
        for i in excluded_paths:
            if i.endswith('*'):
                if path.startswith(i[:1]):
                    return False
        if path in excluded_paths:
            return False
        else:
            return True
    

    def authorization_header(self, request=None) -> str:
        """Get the authorization header from the Flask request object"""
        if request is None:
            return None
        if not request.headers.get("Authorization"):
            return None
        return request.headers.get("Authorization")
    

    def current_user(self, request=None) -> TypeVar('User'):
        """Get the current user from the Flask object"""
        return None