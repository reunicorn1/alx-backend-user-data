#!/usr/bin/env python3
"""A module for filtering logs.
"""
import re
from typing import List, Iterable
import logging


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: Iterable[str], redaction: str, message: str,
                 separator: str,) -> str:
    """
    This function returns the log message obfuscated
    """
    for field in fields:
        message = re.sub(r'(?<={}=)(.*?)(?={})'.format(
            field, separator), redaction, message)
    return message


def get_logger() -> logging.Logger:
    """
    This function creates a logger object
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    console = logging.StreamHandler()
    formatter = RedactingFormatter(PII_FIELDS)

    console.setFormatter(formatter)
    logger.addHandler(console)

    return logger


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: Iterable[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """formats a LogRecord.
        """
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.msg, self.SEPARATOR)
        return super().format(record)
