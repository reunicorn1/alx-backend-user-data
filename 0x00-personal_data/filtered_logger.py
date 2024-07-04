#!/usr/bin/env python3
"""
0. Regex-ing
"""
import re
from typing import List


def filter_datum(fields: List, redaction: str, message: str, seperator: str):
    """
    This function returns the log message obfuscated
    """
    regex = r'({}=).*?(?={}|$)'.format(
            '|'.join(map(re.escape, fields)), re.escape(seperator))
    return re.sub(regex,  r'\1' + redaction, message)
