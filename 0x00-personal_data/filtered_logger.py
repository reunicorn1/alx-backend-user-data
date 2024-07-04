#!/usr/bin/env python3
"""A module for filtering logs.
"""
import os
import re
from typing import List, Iterable
import logging
import mysql.connector


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
    The main entry of the application
    """
    columns = ["name", "email", "phone", "ssn", "password", "ip",
               "last_login" , "user_agent"]
    query = "SELECT {} FROM users;".format(fields)
    info_logger = get_logger()
    connection = get_db()
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            record = map(
                lambda x: '{}={}'.format(x[0], x[1]),
                zip(columns, row),
            )
            msg = '{};'.format('; '.join(list(record)))
            args = ("user_data", logging.INFO, None, None, msg, None, None)
            log_record = logging.LogRecord(*args)
            info_logger.handle(log_record)


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


if __name__ == "__main__":
    main()
