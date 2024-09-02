#!/usr/bin/env python3
"""Module houses the definition of an Authentication class"""

from flask import request
from typing import (
    List,
    TypeVar
)


class Auth:
    """Manages the authentication aspect of the API"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Checkes if a resource requires authentication and acts accordingly
        Args:
            path - the path
            excluded_paths - the excluded path

        Returns:
            False for now
        """
        return False
    
    def authorization_header(self, request=None) -> str:
        """Managest the authorization header
        Args:
            request - the request

        Returns:
            None for now
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Manages a typical user of the application
        Args:
            request - the request

        Returns:
            an instance of the user model
        """
        return None
