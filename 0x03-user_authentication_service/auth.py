#!/usr/bin/env python3
"""This module houses the implementation
of the authentication aspect of the program"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from user import User


def _hash_password(password: str) -> bytes:
    """Hashes a given password

    Args:
        password - a given password to be hashed

    Returns:
        a hashed version of the password is hashed
    """
    hash_pwd: bytes = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return hash_pwd


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
        try:
            user: User = self._db.find_user_by(email=email)
            if user is None:
                return False
        except NoResultFound:
            return False
        if bcrypt.checkpw(password.encode(), user.hashed_password):
            return True
        return False
