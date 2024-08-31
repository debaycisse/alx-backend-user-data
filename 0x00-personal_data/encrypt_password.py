#!/usr/bin/env python3
"""This module contain declaration of a function, named hash_password"""
import bcrypt


def hash_password(password: str) -> bytes:
    """Hashes a given password and returns its hashed salted version

    Returns:
        a salted, hashed version of the given password.
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
