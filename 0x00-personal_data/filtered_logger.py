#!/usr/bin/env python3
"""A module for filtering logs.
"""
import os
import re
from typing import List, Iterable
import logging
import mysql.connector


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
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


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Creates a connector to a database.
    """
    db_host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME", "")
    db_user = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    db_pwd = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    connection = mysql.connector.connection.MySQLConnection(
        host=db_host,
        user=db_user,
        password=db_pwd,
        database=db_name,
    )
    return connection


def main() -> None:
    """
    This is the entry point of the app
    """
    csx = get_db()
    cur = csx.cursor()
    cur.execute("SELECT * FROM users;")
    rows = cur.fetchall()

    logger = get_logger()

    fields = ['name', 'email', 'phone', 'ssn', 'password', 'ip',
              'last_login', 'user_agent']

    for row in rows:
        s = [f"{f}={r.decode('utf-8') if isinstance(r, bytes) else r};"
             for r, f in zip(row, fields)]
        logger.info(" ".join(s))

    cur.close()
    csx.close()


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """formats a LogRecord.
        """
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.msg, self.SEPARATOR)
        return super().format(record)


if __name__ == "__main__":
    main()
