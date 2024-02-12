#!/usr/bin/env python3
""" Module of auth views
"""


from flask import jsonify, abort, request
from api.v1.views import app_views
from typing import List, TypeVar


class Auth:
    """ Auth class"""
    def __init__(self) -> None:
        """initialization"""
        pass

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """require_auth method"""
        return False

    def authorization_header(self, request=None) -> str:
        """authorization_header method"""
        return None

    def current_user(self, request=None):
        """current_user method"""
        return None
