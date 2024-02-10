#!/usr/bin/env python3
"""function called filter_datum that returns the log message obfuscated"""

import re
from typing import List
import logging
import mysql.connector
import os


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(
                fields: List[str],
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


def get_logger() -> logging.Logger:
    """returns a logging object"""
    logger = logging.getLogger('user_data')
    logger.propagate = False
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    formatter = RedactingFormatter(PII_FIELDS)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """returns a connector to the database"""
    connector = mysql.connector.connect(
        user=os.getenv('PERSONAL_DATA_DB_USERNAME', 'root'),
        password=os.getenv('PERSONAL_DATA_DB_PASSWORD', ''),
        host=os.getenv('PERSONAL_DATA_DB_HOST', 'localhost'),
        database=os.getenv('PERSONAL_DATA_DB_NAME'))
    return connector


def main() -> None:
    """main function"""
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM users;')
    users = cursor.fetchall()
    logger = get_logger()
    for user in users:
        message = f"name={user[0]}; email={user[1]}; phone={user[2]}; " + \
            f"ssn={user[3]}; password={user[4]}; ip={user[5]}; " + \
            f"last_login={user[6]}; user_agent={user[7]};"
        logger.info(message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """format the record"""
        return filter_datum(
            self.fields,
            self.REDACTION,
            super().format(record),
            self.SEPARATOR)


if __name__ == "__main__":
    main()
