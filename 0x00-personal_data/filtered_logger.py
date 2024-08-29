#!/usr/bin/env python3
import re
from typing import List

def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
    """Obfuscate specified fields in the log message.

    Args:
        fields (List[str]): A list of field names to be obfuscated.
        redaction (str): The string to replace the sensitive data with.
        message (str): The log message containing the fields to be obfuscated.
        separator (str): The character that separates the fields in the message.

    Returns:
        str: The log message with specified fields obfuscated.
    """
    if not fields or not message:
        raise ValueError("Fields and message must not be empty.")

    # Construct a regex pattern that matches the specified fields followed by their values.
    pattern = r'(?<=' + separator.join([f + '=' for f in fields]) + r')[^' + separator + r']*'
    
    # Use re.sub to replace matched values with the redaction string.
    obfuscated_message = re.sub(pattern, redaction, message)
    
    return obfuscated_message

