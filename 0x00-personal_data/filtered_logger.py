#!/usr/bin/env python3
"""
0. Regex-ing

In the context of computer science, it's crucial to protect PII to maintain
privacy and prevent identity theft. One way to do this is by filtering logs.
"""
import re
from typing import List
import logging


def filter_datum(fields, redaction, message, seperator):
    """ This function returns the log message obfuscated
    """
    for field in fields:
        message = re.sub(r'(?<={}=)(.*?)(?={})'.format(
            field, seperator), redaction, message)
    return message
