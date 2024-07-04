#!/usr/bin/env python3
"""
0. Regex-ing
"""
import re
from typing import List

patterns = {
    'extract': lambda x, y: r'(?P<field>{})=[^{}]*'.format('|'.join(x), y),
    'replace': lambda x: r'\g<field>={}'.format(x),
}


def filter_datum(fields: List, redaction: str, message: str, seperator: str):
    """
    This function returns the log message obfuscated
    """
    extract, replace = (patterns["extract"], patterns["replace"])
    return re.sub(extract(fields, separator), replace(redaction), message)
