# api/v1/auth/session_db_auth.py
from .session_exp_auth import SessionExpAuth
from models.user_session import UserSession

class SessionDBAuth(SessionExpAuth):
    def __init__(self):
        super().__init__()

    def create_session(self, user_id=None):
        session_id = super().create_session(user_id)

        # Create a new UserSession instance and store it in the database
        user_session = UserSession(user_id=user_id, session_id=session_id)
        self.db_session.add(user_session)
        self.db_session.commit()

        return session_id

    def user_id_for_session_id(self, session_id=None):
        if session_id is None:
            return None

        # Query the UserSession in the database based on session_id
        user_session = self.db_session.query(UserSession).filter_by(session_id=session_id).first()

        # Return the user_id from the UserSession if it exists
        return user_session.user_id if user_session else None

    def destroy_session(self, request=None):
        if request and request.current_user:
            # Get the session_id from the request cookie
            session_id = request.cookies.get(self.session_cookie_name)

            # Query the UserSession in the database based on session_id
            user_session = self.db_session.query(UserSession).filter_by(session_id=session_id).first()

            if user_session:
                # Delete the UserSession from the database
                self.db_session.delete(user_session)
                self.db_session.commit()
