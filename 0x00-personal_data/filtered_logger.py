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
    for f in fields:
        message = re.sub(rf'{f}=.+?(?={seperator})',
                         rf'{f}={redaction}', message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class.
        It formats a given data using the below format in the FORNAT variable
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Initializes an instance of this class"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.FIELDS = fields

    def format(self, record: logging.LogRecord) -> str:
        """formats a given record, based on the fields, and other factors"""
        record.msg = filter_datum(self.FIELDS, self.REDACTION,
                                  record.getMessage(), self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)
