#!/usr/bin/env python3
"""This module houses the implementation of a
class that manages the expiration of a session"""

from .session_auth import SessionAuth
from os import getenv
from datetime import (
    datetime,
    timedelta
)


class SessionExpAuth(SessionAuth):
    """Manages the implementation of the session expiration"""

    def __init__(self):
        """Overloads the initialization method of the parent

        Args:
            args - a list of arguments
            kwargs - a list of keyword arguments
        """
        super().__init__()
        self.session_duration = int(getenv("SESSION_DURATION", 0))

    def create_session(self, user_id=None):
        """creates a session with an expiration date's value

        Args:
            user_id - the user's id for which a session id is created

        Returns:
            the created session id if no error, otherwise None
        """ 
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        session_dict = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_dict
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Retrieves a user ID, based on a provided session ID

        Args:
            session_id - the session ID whose
            associated user ID is to be retrieved

        Returns:
            user ID that is associated with
            the given session ID, otherwise None
        """
        if session_id is None:
            return None
        if not (session_id in self.user_id_by_session_id):
            return None
        if self.session_duration <= 0:
            return self.user_id_by_session_id.get(session_id).get("user_id")
        if not ("created_at" in self.user_id_by_session_id.get(session_id)):
            return None
        t_dur = timedelta(seconds=self.session_duration)
        t_dur += self.user_id_by_session_id.get(session_id).get("created_at")
        current_t = datetime.now()
        if t_dur < current_t:
            return None
        return self.user_id_by_session_id.get(session_id).get("user_id")
