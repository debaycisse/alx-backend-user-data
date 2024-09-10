#!/usr/bin/env python3
"""This module houses the implementation of a flask application"""
from flask import (
    Flask,
    jsonify,
    request
)
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'])
def entry_point():
    """Serves the entry point of the program"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def users():
    """Creates a new user object and stores it in a database"""
    email = request.form.get("email")
    password = request.form.get("password")
    if email is None or password is None:
        return jsonify(
            {"message": "Neither email or password can be empty"}
        ), 400
    try:
        AUTH.register_user(email, password)
        return jsonify(
            {"email": "{}".format(email), "message": "user created"}
        )
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
