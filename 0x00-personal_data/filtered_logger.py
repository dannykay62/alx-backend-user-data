#!/usr/bin/env python3
"""a function called filter_datum that returns the log message obfuscated"""
from typing import List
import os
import re
import logging
import mysql.connector
PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str],
                 redaction: str,
                 message: str,
                 separator: str
                 ) -> str:
    """returns the log message obfuscated"""
    """Arguments:
        fields: a list of strings representing all fields to obfuscate
        redaction: a string representing by what the field will be obfuscated
        message: a string representing the log line
        separator: a string representing by which character is separating
        all fields in the log line (message)
        The function should use a regex to replace occurrences of
        certain field values.
        filter_datum should be less than 5 lines long and use re.sub to
        perform the substitution with a single regex.
    """
    for fieldname in fields:
        message = re.sub(f'{fieldname}=.+?{separator}',
                         f"{fieldname}={redaction}{separator}", message)
    return message


class RedactingFormatter(logging.Formatter):
    """Redacting formatter class"""
    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)s-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Initialize redacting formatter"""
        self.fields = list(fields)
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """format method to redact sensitive information"""
        return filter_datum(self.fields,
                            self.REDACTION,
                            super().format(record),
                            self.SEPARATOR)


def get_logger() -> logging.Logger:
    """ returns a logging.Logger object"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(fields=PII_FIELDS))
    logger.addHandler(handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    ----------------------------------------------------------------
    METHOD: get_db function that returns a connector to the database
    ----------------------------------------------------------------
    DESCRIPTION:
    Use the os module to obtain credentials from the environment
    Use the module mysql-connector-python to connect to the MySQL database
    """
    from os import environ
    user = os.environ['PERSONAL_DATA_DB_USERNAME']
    pwd = os.environ['PERSONAL_DATA_DB_PASSWORD']
    host = os.environ['PERSONAL_DATA_DB_HOST']
    db = os.environ['PERSONAL_DATA_DB_NAME']
    return mysql.connector.connect(user=user,
                                   password=pwd,
                                   host=host,
                                   database=db)


if __name__ == "__main__":
    """Main function for the module"""
    db_data = get_db()
    db_query = db_data.cursor()
    db_query.execute('SELECT * FROM users;')
    for rows in db_query:
        print(''.join(str(rows)))
