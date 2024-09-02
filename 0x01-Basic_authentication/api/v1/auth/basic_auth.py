#!/usr/bin/env python3
"""Module houses the definition of a Basic Authentication class"""

from api.v1.auth.auth import Auth


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
