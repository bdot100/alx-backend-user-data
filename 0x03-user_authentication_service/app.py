#!/usr/bin/env python3
"""A Basic flask app
"""
from flask import (
    Flask,
    jsonify,
    request,
    abort
)
from auth import Auth
app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=["GET"], strict_slashes=False)
def welcome():
    """Return a json unsing jsonify message
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def register_user():
    """This route registers new users
    """
    try:
        # Get email and password from form data
        email = request.form.get("email")
        password = request.form.get("password")

        # Use the Auth object to register the user
        user = AUTH.register_user(email, password)

        # If registration is successful, respond with a JSON payload
        response = {
            "email": user.email,
            "message": "user created"
        }
        return jsonify(response), 200

    except ValueError as e:
        # Handle the exception for a user already registered
        response = {
            "message": "email already registered"
        }
        return jsonify(response), 400


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login():
    """This method log in user if the credential is correct
    """
    try:
        # Parse form data to retrieve email and password
        email = request.form.get("email")
        password = request.form.get("password")

        # Check if the provided login information is correct
        if not AUTH.valid_login(email, password):
            # If login information is incorrect, respond with a 401 HTTP status
            abort(401)

        # If login is correct, create a new session for the user
        session_id = AUTH.create_session(email)

        # Store the session ID as a cookie on the response
        response = jsonify({"email": f"{email}", "message": "logged in"})
        response.set_cookie("session_id", session_id)
        return response
    except ValueError as e:
        # Handle any other exceptions or validation errors as needed
        abort(400)  # Bad Request


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
