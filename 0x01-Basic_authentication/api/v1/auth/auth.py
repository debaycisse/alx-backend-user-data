#!/usr/bin/env python3
"""Module houses the definition of an Authentication class"""

from flask import request
from typing import (
    List,
    TypeVar
)


def match_wildcard(path: str, specific_path: str) -> bool:
    """Manages wildcard character in exlcuded path list

    Args:
        path - the path that is to be validated
        specific_path - a path among paths in excluded paths list

    Returns:
        True if the widcard does not include path, otherwise False
    """
    splitted_path = specific_path.split('/')
    for i in range(1, 3):
        if splitted_path[i] not in path:
            return True
    len_main_dir = len(splitted_path[-1])
    if splitted_path[-1][:len_main_dir - 1] not in path:
        return True
    return False


class Auth:
    """Manages the authentication aspect of the API"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Checkes if a resource requires authentication via its url
        Args:
            path - a resource uri to be checked
            excluded_paths - list of excluded resources' uris

        Returns:
            False, if a uri is excluded in the exclusion list, otherwise True
        """
        if (not path) or (not excluded_paths) or (len(excluded_paths) == 0):
            return True
        if path.endswith('/'):
            for p in excluded_paths:
                if p.endswith('*'):
                    return match_wildcard(path, p)
                if not p.endswith('/'):
                    p = p + '/'
                if path == p:
                    return False
            return True
        for p in excluded_paths:
            p_path = path
            if p.endswith('/'):
                if not p_path.endswith('/'):
                    p_path = path + '/'
                if p == p_path:
                    return False
            if p.endswith('*'):
                return match_wildcard(path, p)
            if p_path == p:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """Managest the authorization header
        Args:
            request - the request

        Returns:
            None for now
        """
        if (not request) or (not request.headers.get("Authorization")):
            return None
        return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar('User'):
        """Manages a typical user of the application
        Args:
            request - the request

        Returns:
            an instance of the user model
        """
        return None
