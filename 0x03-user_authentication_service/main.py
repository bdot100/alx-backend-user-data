#!/usr/bin/env python3
"""Main File to test all the endpoints
"""
import requests

BASE_URL = "http://127.0.0.1:5000"  # Replace with your actual server URL


def register_user(email: str, password: str) -> None:
    """
    This method tests the register_user endpoint with the
    given email and password.
    Args:
        email: The email of the user.
        password: The password of the user.
    Returns:
        None
    """
    response = requests.post(f"{BASE_URL}/users", data={"email": email, "password": password})

    if response.status_code == 200:
        assert (response.json() == {"email": email, "message": "user created"})
    else:
        assert(response.status_code == 400)
        assert (response.json() == {"message": "email already registered"})


def log_in_wrong_password(email: str, password: str) -> None:
    """This function tests the login endpoint with a wrong password
    """
    # Implement the log_in_wrong_password function
    # Make a POST request to log in with an incorrect password
    response = requests.post(f"{BASE_URL}/sessions", data={"email": email, "password": password})

    # Assert the expected status code and payload (if any)
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """This tests the login endpoint with the correct details
    """
    # Implement the log_in function
    # Make a POST request to log in with the correct credentials
    response = requests.post(f"{BASE_URL}/sessions", data={"email": email, "password": password})

    # Assert the expected status code and payload (if any)
    assert response.status_code == 200
    assert(response.json() == {"email": email, "message": "logged in"})
    return response.cookies['session_id']


def profile_unlogged() -> None:
    # Implement the profile_unlogged function
    # Make a GET request to the /profile route without a session ID
    response = requests.get(f"{BASE_URL}/profile")
    
    # Assert the expected status code and payload (if any)
    assert response.status_code == 403
    # Add more assertions if needed


def profile_logged(session_id: str) -> None:
    """This tests the profile endpoint with an existing
        detail.
    """
    headers = {"Cookie": f"session_id={session_id}"}
    response = requests.get(f"{BASE_URL}/profile", headers=headers)
    # Assert the expected status code and payload (if any)
    assert response.status_code == 200


def log_out(session_id: str) -> None:
    """Test the logout endpoint
    """
    headers = {"Cookie": f"session_id={session_id}"}
    response = requests.delete(f"{BASE_URL}/sessions", headers=headers)
    
    if response.status_code == 302:
        assert(response.url == 'f"{BASE_URL}/')
    else:
        assert(response.status_code == 200)


def reset_password_token(email: str) -> str:
    # Implement the reset_password_token function
    # Make a POST request to request a reset password token
    response = requests.post(f"{BASE_URL}/reset_password", data={"email": email})
    
    # Assert the expected status code and payload (if any)
    assert response.status_code == 200
    # Extract and return the reset token
    reset_token = response.json()["reset_token"]
    return reset_token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    # Implement the update_password function
    # Make a PUT request to update the password with the reset token
    data = {"email": email, "reset_token": reset_token, "new_password": new_password}
    response = requests.put(f"{BASE_URL}/reset_password", data=data)
    
    # Assert the expected status code and payload (if any)
    assert response.status_code == 200
    # Add more assertions if needed


if __name__ == "__main__":
    EMAIL = "guillaume@holberton.io"
    PASSWD = "b4l0u"
    NEW_PASSWD = "t4rt1fl3tt3"

    # Execute the specified tasks
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
