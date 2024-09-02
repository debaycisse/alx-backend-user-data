#!/usr/bin/env python3
"""This module contain declaration of a function, named hash_password"""
import bcrypt


def hash_password(password: str) -> bytes:
    """Hashes a given password and returns its hashed salted version

    Returns:
        a salted, hashed version of the given password.
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Compares a given hashed password and a plain password for validation

    Args:
        hashed_password - an hashed password to be compared with a plain one
        password - a plain string password to be compared with the hashed one

    Returns:
        True if the plain matches the hashed password, otherwise, False
    """
    return bcrypt.checkpw(password.encode(), hashed_password)
