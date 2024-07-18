#!/usr/bin/env python3
"""
Authentication class
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """Hashing passwords and convertin them to bytes
    """
    bytes = password.encode('utf-8')
    return bcrypt.hashpw(bytes, bcrypt.gensalt())
