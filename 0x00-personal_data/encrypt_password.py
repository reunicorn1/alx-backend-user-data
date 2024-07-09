#!/usr/bin/env python3
"""
Encrypting passwords
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    hashes the password and return a salted hashed byte string
    """
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt)


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    validates if password  matched the hashed password
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
