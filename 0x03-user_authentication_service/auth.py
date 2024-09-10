#!/usr/bin/env python3
'''Auth module'''

import bcrypt


def _hash_password(password: str) -> bytes:
    """Returns a salted hash of the input password"""
    bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(bytes, salt)
    return hash
