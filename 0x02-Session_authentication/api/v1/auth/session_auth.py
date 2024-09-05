#!/usr/bin/env python3
"""This modules houses the definition for the Session Authentication"""

from .auth import Auth
import uuid


class SessionAuth(Auth):
    """Manages session authentication type"""

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """creates a Session ID for a given user_id

        Args:
            user_id - id of a user instance for
            whom a session ID is to be created

        Returns:
            None if error occurs, otherwise a created session id is returned
        """
        if ((user_id is None) or (not isinstance(user_id, str))):
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Retrieves a user ID, based on a provided session ID

        Args:
            session_id - the session ID whose
            associated user ID is to be retrieved

        Returns:
            user ID that is associated with
            the given session ID, otherwise None
        """
        if session_id is None or (not isinstance(session_id, str)):
            return None
        return self.user_id_by_session_id.get(session_id)
