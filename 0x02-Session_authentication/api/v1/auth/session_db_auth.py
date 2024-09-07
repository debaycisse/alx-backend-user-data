#!/usr/bin/env python3
"""This module houses the implementation of a class, named SessionDBAuth"""
from .session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from models.user import User
from uuid import uuid4


class SessionDBAuth(SessionExpAuth):
    """Manages the session data in a database"""

    def create_session(self, user_id=None):
        """Creates a session data for a typical current user and stores it

        Args:
            user_id - an id of the user whose session is to be created

        Returns:
            the created session id, if no error, otherwise None
        """
        if user_id is None:
            return None
        if not isinstance(user_id, str):
            return None
        if len(User.search({"id": user_id})) == 0:
            return None
        # session_id = str(uuid4())

        user_session = UserSession()
        user_session.user_id = user_id
        user_session.session_id = user_session.id
        user_session.save()
        return user_session.id

    def user_id_for_session_id(self, session_id=None):
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
        if UserSession.count() == 0:
            return None
        session_obj_list = UserSession.search({"id": session_id})
        if len(session_obj_list) != 1:
            return None
        return session_obj_list[0].to_json().get("user_id")
    
    def destroy_session(self, request=None):
        """Destroys the UserSession based on the
        Session ID from the request cookie
        
        Args:
            request - the request object that contains
            the session id for the session to be destroyed 
        """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return False
        session
