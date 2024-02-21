#!/usr/bin/env python3
"""
End-to-end integration test
"""


import requests


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"
URL = "http://localhost:5000"


def register_user(email: str, password: str) -> None:
    """test register_user"""
    data = {"email": email, "password": password}
    response = requests.post(f"{URL}/users", data=data)
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "user created"}


def log_in_wrong_password(email: str, password: str) -> None:
    """test log_in_wrong_password"""
    data = {"email": email, "password": password}
    response = requests.post(f"{URL}/sessions", data=data)
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """test log in"""
    data = {"email": email, "password": password}
    response = requests.post(f"{URL}/sessions", data=data)
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "logged in"}
    return response.cookies.get("session_id")


def profile_unlogged() -> None:
    """test profile_unlogged"""
    response = requests.get(f"{URL}/profile")
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """test profile_logged"""
    data = {"session_id": session_id}
    response = requests.get(f"{URL}/profile", cookies=data)
    assert response.status_code == 200
    assert response.json() == {"email": EMAIL}


def log_out(session_id: str) -> None:
    """tet log out"""
    data = {"session_id": session_id}
    response = requests.delete(f"{URL}/sessions", cookies=data)
    assert response.status_code == 200
    assert response.json() == {"message": "Bienvenue"}


def reset_password_token(email: str) -> str:
    """test reset password token"""
    data = {"email": email}
    response = requests.post(f"{URL}/reset_password", data=data)
    assert response.status_code == 200
    reset_tokan = response.json()["reset_token"]
    assert response.json() == {"email": email,
                               "reset_token": reset_tokan}
    return reset_tokan


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """test update password"""
    data = {"email": email,
            "reset_token": reset_token,
            "new_password": new_password}
    response = requests.put(f"{URL}/reset_password", data=data)
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "Password updated"}


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
