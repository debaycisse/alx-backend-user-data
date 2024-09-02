#!/usr/bin/env python3
"""Module houses the definition of a Basic Authentication class"""

from api.v1.auth.auth import Auth
from base64 import standard_b64decode


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
