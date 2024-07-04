#!/usr/bin/env python3
"""
0. Regex-ing
In the context of computer science, it's crucial to protect PII to maintain
privacy and prevent identity theft. One way to do this is by filtering logs.
"""
import re
from typing import List


def filter_datum(fields: List[str], redaction: str, message: str,
                 seperator: str) -> str:
    """
    This function returns the log message obfuscated
    """
    for field in fields:
        message = re.sub(r'(?<={}=)(.*?)(?={})'.format(
            field, seperator), redaction, message)
    return message
