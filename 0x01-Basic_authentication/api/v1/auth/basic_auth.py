#!/usr/bin/env python3
"""basic auth module"""


from api.v1.auth.auth import Auth
import base64
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """basic auth class"""
    def __init__(self) -> None:
        super().__init__()

    def extract_base64_authorization_header(
                                            self,
                                            authorization_header: str) -> str:
        """returns the Base64 part of the
        Authorization header for a Basic Authentication"""
        if (
            authorization_header is None
            or type(authorization_header) is not str
            or not authorization_header.startswith("Basic ")
        ):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(
                                            self,
                                            base64_authorization_header: str
                                            ) -> str:
        """returns the decoded value of a Base64 string"""
        if (
            base64_authorization_header is None
            or type(base64_authorization_header) is not str
        ):
            return None
        try:
            base64_byte = base64.b64decode(
                base64_authorization_header
            )
            return base64_byte.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
                                    self,
                                    decoded_base64_authorization_header: str
                                    ) -> (str, str):
        """returns the user email and password
        from the Base64 decoded value"""
        if (
            decoded_base64_authorization_header is None
            or type(decoded_base64_authorization_header) is not str
            or ':' not in decoded_base64_authorization_header
        ):
            return (None, None)
        return tuple(decoded_base64_authorization_header.split(':', 1))

    def user_object_from_credentials(
                                        self,
                                        user_email: str,
                                        user_pwd: str
                                        ) -> TypeVar('User'):
        '''returns the User instance based on his email and password'''
        if (
            user_email is None
            or type(user_email) is not str
            or user_pwd is None
            or type(user_pwd) is not str
        ):
            return None
        user = User.search({'email': user_email})
        if not user:
            return None
        if not user[0].is_valid_password(user_pwd):
            return None
        return user[0]

    def current_user(self, request=None) -> TypeVar('User'):
        """overloads Auth and retrieves
        the User instance for a request"""
        authorization_header = self.authorization_header(request)
        if authorization_header is None:
            return None
        base64_authorization_header = self.extract_base64_authorization_header(
            authorization_header
        )
        if base64_authorization_header is None:
            return None
        decoded_base64_auth_header = self.decode_base64_authorization_header(
            base64_authorization_header
        )
        if decoded_base64_auth_header is None:
            return None
        user_email, user_pwd = self.extract_user_credentials(
            decoded_base64_auth_header
        )
        if user_email is None or user_pwd is None:
            return None
        return self.user_object_from_credentials(user_email, user_pwd)
