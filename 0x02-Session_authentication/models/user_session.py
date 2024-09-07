#!/usr/bin/env python3
"""This module houses an implementation of a class, named UserSession"""
from .base import (
    Base,
    TIMESTAMP_FORMAT
)


class UserSession(Base):
    """Manages the storage of users' session information"""

    def __init__(self, *args: list, **kwargs: dict):
        """Initializes an instance of this class
        
        Args:
            args - list of passed arguments
            kwargs - list of keyword arguments
        """
        super().__init__(*args, **kwargs)
        self.user_id = ""
        self.session_id = ""
