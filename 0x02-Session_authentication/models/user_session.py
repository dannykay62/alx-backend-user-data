# models/user_session.py
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class UserSession(Base):
    __tablename__ = 'user_session'

    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey('user.id'), nullable=False)
    session_id = Column(String, nullable=False)

    user = relationship('User', back_populates='sessions')

    def __init__(self, user_id: str, session_id: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_id = user_id
        self.session_id = session_id
