#!/usr/bin/env python3
""" SessionAuth view module """

from models.user import User
from flask import jsonify
from api.v1.app import app_views
from flask import request, abort
from api.v1.auth.session_auth import SessionAuth
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    '''handles all routes for the Session authentication'''
    email = request.form.get(key='email')
    password = request.form.get(key='password')
    if not email or email == '':
        return jsonify({"error": "email missing"}), 400
    if not password or password == '':
        return jsonify({"error": "password missing"}), 400
    users = User.search({'email': email})
    if not users or len(users) == 0:
        return jsonify({"error": "no user found for this email"}), 404
    for user in users:
        if user.is_valid_password(password):
            from api.v1.app import auth
            session_id = auth.create_session(user.id)
            resp = jsonify(user.to_json())
            session_name = os.getenv('SESSION_NAME')
            resp.set_cookie(session_name, session_id)
            return resp
    return jsonify({"error": "wrong password"}), 401

@app_views.route('/api/v1/auth_session/logout', methods=['DELETE'], strict_slashes=False)
def logout():
    '''ends the session and logs user out'''
    from api.v1.app import auth
    check = auth.destroy_session(request)
    if not check or check == False:
        abort(404)
    return jsonify({}), 200
