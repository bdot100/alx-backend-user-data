#!/usr/bin/env python3
"""A Basic flask app
"""
from flask import (
    Flask,
    jsonify,
    request
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
