#!/usr/bin/env python3
"""This module houses an implementation
of an end-to-end integration testing"""

import requests


_URL = "http://localhost:5000/{}"


def register_user(email: str, password: str) -> None:
    """Registers a new user and stores them into the database
    
    Args:
        email - email address of the new user
        password - password of the new user
    """
    data = {"email": email, "password": password}
    response = requests.post(_URL.format('users'), data = data)
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "user created"}

def log_in_wrong_password(email: str, password: str) -> None:
    """Tests that wrong password is rejected
    
    Args:
        email - email address of an existing user
        password - wrong password of an existing user
    """
    data = {"email": email, "password": password}
    response = requests.post(_URL.format('sessions'), data = data)
    assert response.status_code == 401

def log_in(email: str, password: str) -> str:
    """Tests that an existing user can login

    Args:
        email - email address of an existing user
        password - password of an existing user
    """
    data = {"email": email, "password": password}
    response = requests.post(_URL.format('sessions'), data = data)
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "logged in"}
    return response.cookies['session_id']

def profile_unlogged() -> None :
    """Tests the behavior of visiting a profile end
    point by a user who is not logged"""

    cookies = {'session_id': None}
    response = requests.get(_URL.format('profile'), cookies = cookies)
    assert response.status_code == 403

def profile_logged(session_id: str) -> None:
    """Tests that profile end point works well with a correct session id

    Args:
        session_id - value of a valid session id
    """
    cookies = {'session_id': session_id}
    response = requests.get(_URL.format('profile'), cookies = cookies)
    assert response.status_code == 200
    assert response.json() == {"email": "guillaume@holberton.io"}

def log_out(session_id: str) -> None:
    """Tests that user is logged out correctly

    Args:
        session_id - the session id of the current user, to be logged out
    """
    data = {"session_id": session_id}
    response = requests.delete(_URL.format('sessions'), data = data)
    assert response.status_code == 302

def reset_password_token(email: str) -> str:
    """Tests that password token endpoint works correctly

    Args:
        email - email of an existing user to test with

    Returns:
        the password reset token is returned
    """
    data = {"email": email}
    response = requests.post(_URL.format('reset_password'), data = data)
    assert response.status_code == 200
    reset_token = response.json().get("reset_token")
    assert response.json() == {"email": email, "reset_token": reset_token}
    return reset_token

def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Tests that the endpoint that updates the password works as expected

    Args:
        email - email of an existing user
        reset_token - the reset token' value, previously requested
        new_password - new password to change to
    """
    data = dict(email = email,
                reset_token = reset_token,
                new_password = new_password)
    response = requests.put(_URL.format('reset_password'), data = data)
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "Password updated"}
    

EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


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
