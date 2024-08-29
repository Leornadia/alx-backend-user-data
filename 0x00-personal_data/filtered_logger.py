#!/usr/bin/env python3
import logging
from typing import List, Tuple
from re import sub
import os
import mysql.connector
from mysql.connector.connection import MySQLConnection

# Define the PII_FIELDS constant
PII_FIELDS: Tuple[str, ...] = ("name", "email", "phone", "ssn", "password")

def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
    """
    Obfuscate specific fields in a log message.

    Args:
        fields (List[str]): List of fields to obfuscate.
        redaction (str): The string to replace the field values with.
        message (str): The log message.
        separator (str): The character separating the key-value pairs.

    Returns:
        str: The obfuscated log message.
    """
    pattern = f'({"|".join(fields)})=.*?(?={separator}|$)'
    return sub(pattern, lambda m: f'{m.group(1)}={redaction}', message)

class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """ Initialize the formatter with fields to redact """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the log record, obfuscating PII fields.

        Args:
            record (logging.LogRecord): The log record.

        Returns:
            str: The formatted log message with obfuscated PII fields.
        """
        record.msg = filter_datum(self.fields, self.REDACTION, record.msg, self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)

def get_logger() -> logging.Logger:
    """
    Create and configure a logger.

    Returns:
        logging.Logger: The configured logger.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    # Create a StreamHandler with the RedactingFormatter
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(fields=PII_FIELDS))

    # Add the handler to the logger
    logger.addHandler(stream_handler)

    return logger

def get_db() -> MySQLConnection:
    """
    Connect to a MySQL database using credentials from environment variables.

    Returns:
        MySQLConnection: A MySQL connection object.
    """
    # Get database credentials from environment variables
    user = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    database = os.getenv('PERSONAL_DATA_DB_NAME')

    # Connect to the database
    return mysql.connector.connect(
        user=user,
        password=password,
        host=host,
        database=database
    )

def main() -> None:
    """
    Main function that retrieves all rows from the users table
    and logs them with sensitive information obfuscated.
    """
    # Get the logger and database connection
    logger = get_logger()
    db = get_db()
    
    # Execute a query to retrieve all rows from the users table
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    
    # Fetch all rows
    rows = cursor.fetchall()
    
    # Define the field names in the correct order
    field_names = [desc[0] for desc in cursor.description]
    
    # Log each row
    for row in rows:
        # Create the log message
        message = "; ".join([f"{field}={value}" for field, value in zip(field_names, row)]) + ";"
        # Log the message
        logger.info(message)
    
    # Close the cursor and database connection
    cursor.close()
    db.close()

if __name__ == "__main__":
    main()

