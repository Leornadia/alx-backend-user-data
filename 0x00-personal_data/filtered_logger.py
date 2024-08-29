#!/usr/bin/env python3
import logging
from typing import List
from re import sub

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
    """ Redacting Formatter class
    """

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

