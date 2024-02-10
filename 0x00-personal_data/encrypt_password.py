#!/usr/bin/env python3
"""hash_password function that expects
one string argument name password and returns a salted,
hashed password, which is a byte string."""

import bcrypt


def hash_password(password: str) -> bytes:
    """returns a salted, hashed password"""
    password = bytes(password, 'utf-8')
    return bcrypt.hashpw(password, bcrypt.gensalt())
