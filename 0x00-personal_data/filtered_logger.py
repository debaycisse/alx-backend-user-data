#!/usr/bin/env python3
"""This module houses declaration for a function, named
filter_datum and other functions that helps in redacting a PII data"""
import re
import os
from mysql.connector import connect  # type: ignore
from typing import (
    Sequence,
    Tuple,
    List
)
import logging


def filter_datum(fields: List[str], redaction: str,
                 message: str, seperator: str) -> str:
    """Obfuscates a given message, based on a given fields

    Args:
        fields - a list of strings representing all fields to obfuscate
        redaction - a string representing by what the field will be obfuscated
        message - a string representing the log line
        separator - a string representing a character, separating all fields

    Returns:
        returns an obfuscated version of the passed message
    """
    for field in fields:
        message = re.sub(rf'{field}=.+?(?={seperator})',
                         rf'{field}={redaction}', message)
    return message
