#!/usr/bin/env python3
"""_hash_password method"""


import bcrypt


def _hash_password(password: str) -> str:
    """returns bytes"""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
