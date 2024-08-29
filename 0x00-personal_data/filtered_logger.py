#!/usr/bin/env python3
import os
import mysql.connector
from mysql.connector import connection
import logging
from typing import List

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


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
        record.msg = filter_datum(self.fields, self.REDACTION, record.msg, self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)


def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
    """ Returns the log message obfuscated """
    for field in fields:
        message = re.sub(rf'{field}=[^{separator}]*', f'{field}={redaction}', message)
    return message


def get_logger() -> logging.Logger:
    """ Returns a logging.Logger object """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(fields=PII_FIELDS)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger


def get_db() -> connection.MySQLConnection:
    """ Connects to the database using credentials from environment variables """
    username = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    database = os.getenv('PERSONAL_DATA_DB_NAME')

    conn = mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        database=database
    )
    
    return conn


def main():
    """ Main function to retrieve and display all rows in the users table """
    db = get_db()
    cursor = db.cursor()

    # Execute the query to fetch all rows from the users table
    cursor.execute("SELECT name, email, phone, ssn, password, ip, last_login, user_agent FROM users;")
    
    # Setup logger
    logger = get_logger()

    # Log each row with filtered data
    for row in cursor.fetchall():
        log_message = (
            f"name={row[0]}; email={row[1]}; phone={row[2]}; ssn={row[3]}; "
            f"password={row[4]}; ip={row[5]}; last_login={row[6]}; user_agent={row[7]};"
        )
        logger.info(log_message)
    
    cursor.close()
    db.close()

if __name__ == "__main__":
    main()

