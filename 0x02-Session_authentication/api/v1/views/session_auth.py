#!/usr/bin/env python3
"""
view that handles all routes for the Session
authentication.
"""
from flask import Flask, Blueprint, request, jsonify, make_response
from api.v1.views import app_views
from models.user import User
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def auth_session():
    """
    This route handles user login
    Return:
        The dict repr of the user if found else:
            Return: Error Message
    """
    # Get the email and password from the request form
    email = request.form.get('email')
    password = request.form.get('password')

    # check if email is missing or empty
    if not email:
        return jsonify({"error": "email missing"}), 400

    # Check if password is missing
    if not password:
        return jsonify({"error": "password missing"}), 400

    # Retrive the user instance based on the email
    users = User.search({"email": email})

    # If no User found, return a 404 error
    if not users or users == []:
        return jsonify({"error": "no user found for this email"}), 404

    for user in users:
        # Check if the password is correct
        if user.is_valid_password(password):
            from api.v1.app import auth
            # Create a Session ID for the User ID
            session_id = auth.create_session(user.id)
            response_data = jsonify(user.to_json())
            session_name = os.getenv('SESSION_NAME')
            response_data.set_cookie(session_name, session_id)
            return response_data, 200
        return jsonify({"error": "wrong password"}), 401
