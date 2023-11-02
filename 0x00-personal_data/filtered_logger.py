#!/usr/bin/env python3
"""a function called filter_datum that returns the log message obfuscated"""
from typing import List
import os
import re
import logging
# import mysql.connector
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

    def __ini__(self, fields: List[str]):
        """Initialize redacting formatter"""
        self.fields = list(fields)
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """format method to redact sensitive information"""
        return filter_datum(self.fields,
                            self.REDACTION,
                            super().format(record),
                            self.SEPARATOR)
