#!/usr/bin/env python3
"""
Session authentication view
"""
from api.v1.views import app_views
from flask import abort, jsonify, request, make_response
from models.user import User
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def view_session_login() -> str:
    """ POST /api/v1/auth_session/login
    Return:
        - the user onkect JSON represented
    """
    email, password = request.form.get('email'), request.form.get('password')
    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400
    users = User.search({'email': email})
    if not users or not len(users):
        return jsonify({"error": "no user found for this email"}), 404
    if not users[0].is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401
    from api.v1.app import auth
    _id = auth.create_session(users[0].id)
    resp = make_response(users[0].to_json())
    resp.set_cookie(os.getenv('SESSION_NAME'), _id)
    return resp
