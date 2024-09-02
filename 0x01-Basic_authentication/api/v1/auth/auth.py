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
        if (not path) or (not excluded_paths) or (len(excluded_paths) == 0):
            return True
        if path.endswith('/'):
            for p in excluded_paths:
                if not p.endswith('/'):
                    p = p + '/'
                if path == p:
                    return False
        for p in excluded_paths:
            p_path = path
            if p.endswith('/'):
                p_path = path + '/'
            if p == p_path:
                return False
        return True

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
