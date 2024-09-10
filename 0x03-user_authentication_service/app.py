#!/usr/bin/env python3
"""Flask app module"""

from flask import Flask, jsonify, request, abort, make_response, redirect
from auth import Auth
from sqlalchemy.orm.exc import NoResultFound


app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=['GET'], strict_slashes=False)
def mainRoute():
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=['POST'], strict_slashes=False)
def users():
    email = request.form.get(key='email')
    password = request.form.get(key='password')
    try:
        AUTH._db.find_user_by(email=email)
        return jsonify({"message": "email already registered"}), 400
    except NoResultFound:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"}), 200


@app.route("/sessions", methods=['POST'], strict_slashes=False)
def login():
    """Handles the login process"""
    email = request.form.get(key='email')
    password = request.form.get(key='password')
    exist = AUTH.valid_login(email, password)
    if exist is False:
        abort(401)
    session_id = AUTH.create_session(email)
    res = make_response(
            jsonify({"email": email, "message": "logged in"}), 200)
    res.set_cookie("session_id", session_id)
    return res


@app.route("/sessions", methods=['DELETE'], strict_slashes=False)
def logout() -> str:
    """Handles the logout process"""
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect('/')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
