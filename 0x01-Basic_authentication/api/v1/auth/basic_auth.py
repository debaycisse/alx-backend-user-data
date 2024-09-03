#!/usr/bin/env python3
"""Module houses the definition of a Basic Authentication class"""

from api.v1.auth.auth import Auth
from base64 import standard_b64decode
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """Handles basic authentication scheme"""

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """Extracts the base 64 part of an authorization header

        Args:
            authorization_header - a given authorization header to be extracted

        Returns:
            the base 64 part of the authorization header if the
            authorization header is not none, else None
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """Decodes a given base 64 string

        Args:
            base64_authorization_header - the base64 string to be decoded

        Returns:
            the decoded value is returned, if the
            given string is not none, otherwise none
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        decoded_value = None
        try:
            decoded_value = standard_b64decode(base64_authorization_header)
        except Exception:
            return None
        return decoded_value.decode('utf-8')

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> (str, str):
        """Extracts the credentials of a user from
        the given decoded base 64 authorization header

        Args:
            decoded_base64_authorization_header - credentials
            are extracted from here

        Returns:
            a tuple of both user's email and password if a given
            decode base 64 is not none, otherwise none
        """
        if decoded_base64_authorization_header is None:
            return (None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)
        cred = decoded_base64_authorization_header.split(":")
        return (cred[0], cred[1])

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """Retrieves a user's instance, based a provided email and password

        Args:
            user_email - the email address of a user to be retrieved
            user_pwd - password of a user whose instance is to be retrieved

        Returns:
            a user's instance that matches the given
            credentials or none if user does not exists
        """
        if ((not user_email) or (not user_pwd)):
            return None
        if ((not isinstance(user_email, str)) or
           (not isinstance(user_pwd, str))):
            return None
        if User.count() == 0:
            return None
        _user = User.search({"email": user_email})
        if len(_user) > 0:
            _user = _user[0]
            if _user.is_valid_password(user_pwd):
                return _user
        return None
