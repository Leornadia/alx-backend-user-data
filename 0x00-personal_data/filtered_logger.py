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
    # Create a regex pattern that matches the specified fields followed by their values
    pattern = r'(' + '|'.join(re.escape(field) for field in fields) + r')=' + r'[^' + re.escape(separator) + r']*'
    
    # Replace the matched values with the redaction string
    return re.sub(pattern, lambda m: f'{m.group(1)}={redaction}', message)

# Example usage
if __name__ == "__main__":
    fields = ["password", "date_of_birth"]
    messages = [
        "name=egg;email=eggmin@eggsample.com;password=eggcellent;date_of_birth=12/12/1986;",
        "name=bob;email=bob@dylan.com;password=bobbycool;date_of_birth=03/04/1993;"
    ]
    
    for message in messages:
        print(filter_datum(fields, 'xxx', message, ';'))

