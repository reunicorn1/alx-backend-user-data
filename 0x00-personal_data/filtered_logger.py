#!/usr/bin/env python3
"""
0. Regex-ing
"""
import re
from typing import List


def filter_datum(fields: List, redaction: str, message: str, seperator: str):
    """
    This function returns the log message obfuscated
    a
    very
    long
    docstring
    """
    for field in fields:
         regex = '(?<={}=)(.*?)(?={})'.format(field, seperator)
         message = re.sub(regex, redaction, message)
     return messagere.sub(pattern(fields, seperator), r'\1' + redaction, message)
