#!/usr/bin/env python3
"""function called filter_datum that returns the log message obfuscated"""

import re


def filter_datum(
                fields: list,
                redaction: str,
                message: str,
                separator: str) -> str:
    """returns the log message obfuscated"""
    for field in fields:
        message = re.sub(
            f"{field}=.+?{separator}",
            f"{field}={redaction}{separator}",
            message)
    return message
