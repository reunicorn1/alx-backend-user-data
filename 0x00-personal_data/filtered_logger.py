#!/usr/bin/env python3
"""A module for filtering logs.
"""
import re
from typing import List


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str,) -> str:
    """
    This function returns the log message obfuscated
    """
    for field in fields:
        message = re.sub(r'(?<={}=)(.*?)(?={})'.format(
            field, separator), redaction, message)
    return message
