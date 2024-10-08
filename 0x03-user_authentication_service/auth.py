#!/usr/bin/env python3
"""This module houses the implementation
of the authentication aspect of the program"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from user import User
from uuid import uuid4
from typing import Union


def _hash_password(password: str) -> bytes:
    """Hashes a given password

    Args:
        password - a given password to be hashed

    Returns:
        a hashed version of the password is hashed
    """
    hash_pwd: bytes = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return hash_pwd


def _generate_uuid() -> str:
    """Generates uuid and returns it string representation

    Returns:
        string reprensentation of the uuid
    """
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication
database.
    """
    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Registers a new user and stores the user's data in the database

        Args:
            email - email of the new user
            password - password of the new user

        Returns:
            the uswr object of the new user, if no error, otherwise an error
        """
        try:
            user: User = self._db.find_user_by(email=email)
            if not (user is None):
                raise ValueError("User {0} already exists".format(email))
        except NoResultFound:
            pwd: bytes = _hash_password(password)
            user = self._db.add_user(email, pwd)
        return user

    def valid_login(self, email: str, password: str) -> bool:
        """Validates a given user's credentials and indicates if it is valid

        Args:
            email - an email of the user whose credentials are to be validated
            password - the password of the user

        Returns:
            True if the credentials are correct, otherwise False
        """
        if email is None or password is None:
            return False
        if (not isinstance(email, str)) or (not isinstance(password, str)):
            return False
        try:
            user: User = self._db.find_user_by(email=email)
            if user is None:
                return False
        except NoResultFound:
            return False
        if bcrypt.checkpw(password.encode(), user.hashed_password):
            return True
        return False

    def create_session(self, email: str) -> Union[str, None]:
        """Retrieves a session id of a given user's email attribute

        Args:
            email - the email of a given user

        Returns:
            the session id, associated to a user is returned
        """
        if (email is None) or (not isinstance(email, str)):
            return None
        session_id: Union[str, None] = None
        try:
            user: User = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
        except NoResultFound:
            return None
        return session_id

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """Retrieves a user object via its session id attribute

        Args:
            session_id - the value of the session id for a user to look up

        Returns:
            a user's instance if found, otherwise None
        """
        if (session_id is None) or (not isinstance(session_id, str)):
            return None
        user: Union[User, None] = None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        if user is None:
            return None
        return user

    def destroy_session(self, user_id) -> None:
        """Destroys a user's session from the database

        Args:
            user_id - identifier value for the user
            whose session is to be destroyed
        """
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """Finds the corresponding user of the email
        and generates a password reset token for it

        Args:
            email - the email of the user whose
            password reset token is to be generated

        Returns:
            the generated password reset token
        """
        user: User = self._db.find_user_by(email=email)
        if user is None:
            raise ValueError("User does not exists")
        reset_token = _generate_uuid()
        self._db.update_user(user.id, reset_token=reset_token)
        return reset_token

    def update_password(self, reset_token: str, password: str):
        """Resets a password by updating user's password

        Args:
            reset_token - a password rest token
            password - a new password's value
        """
        user: User = self._db.find_user_by(reset_token=reset_token)

        if user is None:
            raise ValueError("User does not exists")
        hash_pwd: bytes = _hash_password(password)
        self._db.update_user(user.id,
                             hashed_password=hash_pwd,
                             reset_token=None)
