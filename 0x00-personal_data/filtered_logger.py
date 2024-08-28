#!/usr/bin/env python3
import re
from typing import List

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
    return re.sub(f'({"|".join(fields)})=[^{separator}]+', f'\\1={redaction}', message)

