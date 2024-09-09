#!/usr/bin/env python3
"""This module houses the implementation
of the authentication aspect of the program"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """Hashes a given password

    Args:
        password - a given password to be hashed

    Returns:
        a hashed version of the password is hashed
    """
    hash_pwd = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return hash_pwd
