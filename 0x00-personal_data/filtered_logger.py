#!/usr/bin/env python3
"""
0. Regex-ing
"""
import re
from typing import List


def filter_datum(fields: List, redaction: str, message: str, seperator: str):
    """This function returns the log message obfuscated"""
    for field in fields:
        regex = '(?<={}=)(.*?)(?={})'.format(field, seperator)
        message = re.sub(regex, redaction, message)
    retrn message
