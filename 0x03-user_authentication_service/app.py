#!/usr/bin/env python3
"""Flask app module"""

from flask import Flask, jsonify, request
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
