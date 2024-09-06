#!/usr/bin/env python3
"""This modules houses the definition for the Session Authentication"""

from .auth import Auth
from models.user import User
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
        if (session_id is None) or not (type(session_id) is str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """Retrieves a user's instance based
        on the cookie, passed in a request

        Args:
            request - the request object
            that contains the cookie among other data

        Returns:
            an instance of a user class is returned, if found, otherwise None
        """
        if request is None:
            return None
        session_id = self.session_cookie(request=request)
        if session_id is None:
            return None
        user_id = self.user_id_for_session_id(session_id)
        if user_id:
            return User.get(user_id)
        return None

    def destroy_session(self, request=None):
        """Destroys existing session by deleting a current user's session

        Args:
            request - a request object from a user or client
        """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return False
        del self.user_id_by_session_id[session_id]
        return True
