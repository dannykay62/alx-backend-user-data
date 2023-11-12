#!/usr/bin/env python3
"""Adding session expiration to the two authentication systems"""
from api.v1.auth.session_auth import SessionAuth
from os import getenv
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """Session expiration class that inherits from SessionAuth"""
    def __init__(self):
        """Constructor for SessionExpAuth class"""
        super().__init__()

        """Assign duration attribute"""
        session_duration_env = getenv("SESSION_DURATION")
        try:
            self.session_duration = int(
                session_duration_env) if session_duration_env else 0
        except ValueError:
            self.session_duration = 0

        def create_session(self, user_id=None):
            """Create a session ID with expiration"""
            session_id = SessionAuth.create_session(user_id)
            """if super can not create a session ID return None"""
            if session_id is None:
                return None
            """in the user_id_session_id dictionary, use a Session ID as key"""
            self.user_id_by_session_id[session_id] = {
                "user": user_id,
                "created_at": datetime.now()
            }

            return session_id

    def user_id_for_session_id(self, session_id: str = None):
        """Overload function - return user_id for a
        given Session ID with expiration """
        if session_id is None:
            return None

        session_dict = self.user_id_by_session_id.get(session_id)
        """If session_dict is None, return None"""
        if session_dict is None or session_dict.get("user_id") is None:
            return None

        """return user_id if session_duration is negative or 0"""
        if self.session_duration <= 0:
            return session_dict["user_id"]

        created_at = session_dict["created_at"]
        """if created_at is not present, return None"""
        if created_at is None:
            return None
        """now calculate the expiry time"""
        expiration_time = created_at + timedelta(seconds=self.session_duration)
        """if the session has expired, return None"""
        if expiration_time < datetime.now():
            return None
        return session_dict["user_id"]
