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
        if path and path[-1] != '/':
            path += '/'
        if (
            path is None
            or excluded_paths is None
            or len(excluded_paths) == 0
            or path not in excluded_paths
        ):
            return True
        return False

    def authorization_header(self, request=None) -> str:
        """authorization_header method"""
        if request is None or "Authorization" not in request.headers:
            return None
        return request.headers["Authorization"]

    def current_user(self, request=None):
        """current_user method"""
        return None


class BasicAuth(Auth):
    """basic auth class"""
    pass
