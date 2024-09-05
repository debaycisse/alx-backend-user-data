from flask import jsonify, abort, request
from api.v1.views import app_views
from models.user import User
from os import getenv


@app_views.route("/auth_session/login",
                 methods=["POST"], strict_slashes=False)
def login():
    """Logs an existing user in to the system"""
    email = request.form.get("email")
    if email is None:
        return jsonify({"error": "email missing"}), 400
    password = request.form.get("password")
    if password is None:
        return jsonify({"error": "password missing"}), 400
    user = User.search({"email": email})
    if len(user) <= 0:
        return jsonify({"error": "no user found for this email"}), 404
    user = user[0]
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401
    from api.v1.app import auth
    session_id = auth.create_session(user.id)
    cookie_name = getenv("SESSION_NAME")
    response_data = jsonify(user.to_json())
    response_data.set_cookie(cookie_name, session_id)
    return response_data


@app_views.route("/auth_session/logout",
                 methods=["DELETE"], strict_slashes=False)
def logout():
    """Logs a current user out of the system"""
    from api.v1.app import auth
    if not auth.destroy_session(request):
        abort(404)
    return jsonify({}), 200
