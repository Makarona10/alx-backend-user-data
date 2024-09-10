#!/usr/bin/env python3
"""Flask app module"""

from flask import Flask, jsonify, request, abort
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
    request.cookies.session_id = session_id
    return jsonify({"email": email, "message": "logged in"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
