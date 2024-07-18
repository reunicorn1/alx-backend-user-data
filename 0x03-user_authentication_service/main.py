#!/usr/bin/env python3
"""
Main Entry Point
"""
import requests
import json


def register_user(email: str, password: str) -> None:
    """
    This method tests registering a user to the database
    """
    args = {"email": email, "password": password}
    x = requests.post(URL + '/users', data=args)

    #  Test normal creation
    assert x.status_code == 200
    assert json.loads(x.content.decode('utf-8')) == {
            "email": email,
            "message": "user created"
            }

    #  Test a duplicate value
    y = requests.post('http://127.0.0.1:5000/users', data=args)
    assert y.status_code == 400
    assert json.loads(y.content.decode('utf-8')) == {
            "message": "email already registered"
            }


def log_in_wrong_password(email: str, password: str) -> None:
    """
    This method tests a log in with the wrong credentials
    """
    args = {"email": email, "password": password}
    x = requests.post(URL + '/sessions', data=args)

    #  Test with wrong password
    assert x.status_code == 401


def log_in(email: str, password: str) -> str:
    """
    This method tests a normal log in process
    """
    args = {"email": email, "password": password}
    x = requests.post(URL + '/sessions', data=args)

    #  Tests logging in as a user
    assert x.status_code == 200
    assert json.loads(x.content.decode('utf-8')) == {
            "email": f"{email}",
            "message": "logged in"
            }
    return x.cookies.get("session_id")


def profile_unlogged() -> None:
    """
    This method attempts to login without a session_id
    """
    x = requests.get(URL + '/profile')
    assert x.status_code == 403


def profile_logged(session_id: str) -> None:
    """
    This method tries to log in to the profile of the user using the
    session_id
    """
    cookies = {"session_id": session_id}
    x = requests.get(URL + '/profile', cookies=cookies)

    #  Tests correct log in
    assert x.status_code == 200
    assert "email" in json.loads(x.content.decode('utf-8'))


def log_out(session_id: str) -> None:
    """
    This function attempts to log the user out of the server sessions
    """
    cookies = {"session_id": session_id}
    x = requests.delete(URL + '/sessions', cookies=cookies)

    #  Tests correct logout
    assert x.status_code == 200
    assert json.loads(x.content.decode('utf-8')) == {
            "message": "Bienvenue"
            }
    #  Tests incorrect logout
    y = requests.delete(URL + '/sessions')
    assert y.status_code == 403


def reset_password_token(email: str) -> str:
    """
    This function attempts to reset the password for a user
    """
    args = {"email": email}
    x = requests.post(URL + '/reset_password', data=args)
    return_value = json.loads(x.content.decode('utf-8'))

    #  Tests correct data
    assert x.status_code == 200
    assert "email" in return_value and "reset_token" in return_value

    #  Tests incomplete data
    y = requests.post(URL + '/reset_password', data={"email": "nope"})
    assert y.status_code == 403

    return return_value["reset_token"]


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """
    This method attempts to update a password after reseting the
    password token
    """
    args = {"email": email, "reset_token": reset_token,
            "new_password": new_password}
    x = requests.put(URL + '/reset_password', data=args)

    # Tests correct data
    assert x.status_code == 200
    assert json.loads(x.content.decode('utf-8')) == {
            "email": f"{email}",
            "message": "Password updated"
            }


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"
URL = "http://127.0.0.1:5000"

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
