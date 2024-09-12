#!/usr/bin/env python3
"""
Auth module
"""
import bcrypt

def _hash_password(password: str) -> bytes:
    """
    Hash a password using bcrypt and return the salted hash as bytes.

    Args:
        password (str): The password to hash.

    Returns:
        bytes: The salted hash of the password.
    """
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    
    return hashed_password

