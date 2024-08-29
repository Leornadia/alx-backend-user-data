#!/usr/bin/env python3
"""
Module for filtering PII data
"""
import logging
import re
import mysql.connector
import os
from typing import Tuple, List, Any


def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
  """
  Returns the log message obfuscated.
  """
  for field in fields:
    message = re.sub(f'{field}=([^;]*)', f'{field}={redaction}', message)
  return message

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
        """
        Filters values in incoming log records.
        """
        return filter_datum(self.fields, self.REDACTION, record.getMessage(), self.SEPARATOR)

PII_FIELDS: Tuple[str, ...] = ("name", "email", "phone", "ssn", "password")

def get_logger() -> logging.Logger:
    """
    Returns a logging.Logger object.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(handler)
    return logger

def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Returns a connector to the database.
    """
    username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    database = os.getenv("PERSONAL_DATA_DB_NAME")
    return mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        database=database
    )

def main():
    """
    Main function.
    """
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    for row in cursor:
        logger = get_logger()
        logger.info(f"{row}")
    cursor.close()
    db.close()

if __name__ == "__main__":
    main()
