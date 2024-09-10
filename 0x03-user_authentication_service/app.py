#!/usr/bin/env python3
"""This module houses the implementation of a flask application"""
from flask import (
    Flask,
    jsonify,
    request,
    abort,
    Response
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


@app.route('/sessions', methods=['POST'])
def login():
    """Logs a typical user in to the system"""
    email: str = request.form.get("email")
    password: str = request.form.get("password")
    if not (AUTH.valid_login(email, password)):
        abort(401)
    session_id: str = AUTH.create_session(email)
    res_obj: Response = jsonify(
        {"email": "{}".format(email), "message": "logged in"}
    )
    res_obj.set_cookie("session_id", session_id)
    return res_obj


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
