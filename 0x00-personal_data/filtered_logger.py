#!/usr/bin/env python3
"""A module for filtering logs.
"""
import os
import re
import logging
import mysql.connector
from typing import List


def filter_datum(
        fields: List[str], redaction: str, message: str, separator: str,
        ) -> str:
    """Filters a log line.
    """
    for field in fields:
        message = re.sub(r'(?<={}=)(.*?)(?={})'.format(
            field, separator), redaction, message)
    return message
