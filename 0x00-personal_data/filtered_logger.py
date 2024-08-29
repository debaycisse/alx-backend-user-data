#!/usr/bin/env python3
"""This module houses declaration for a function, named filter_datum"""
import re
from typing import (
    Sequence,
    Tuple
)
import logging


PII_FIELDS: Tuple[str, ...] = ('name', 'email', 'phone', 'ssn', 'password')


def get_logger() -> logging.Logger:
    """returns a logger object"""
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(stream_handler)
    return logger


def filter_datum(fields: Sequence, redaction: str,
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


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: Tuple[str, ...]):
        """Initializes an instance of this class"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.FIELDS = fields

    def format(self, record: logging.LogRecord) -> str:
        """formats a given record, based on the fields, and other factors"""
        record.msg = filter_datum(self.FIELDS, self.REDACTION,
                                  record.getMessage(), self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)
