#!/usr/bin/env python3
"""flask app"""


from flask import Flask, jsonify, request, abort, redirect
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route("/")
def index():
    """index route"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def register():
    """register new user"""
    try:
        email = request.form["email"]
        password = request.form["password"]
    except KeyError:
        abort(400)

    try:
        user = AUTH.register_user(email, password)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400

    return jsonify({"email": email, "message": "user created"})


@app.route("/sessions", methods=["POST"])
def login():
    """login"""
    try:
        email = request.form["email"]
        password = request.form["password"]
    except KeyError:
        abort(400)

    session_id = AUTH.create_session(email)
    if not session_id or not AUTH.valid_login(email, password):
        abort(401)
    make_response = jsonify({"email": email, "message": "logged in"})
    make_response.set_cookie("session_id", session_id)
    return make_response, 200


@app.route("/sessions", methods=["DELETE"])
def logout():
    """logout"""
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        return redirect("/")
    abort(403)


@app.route("/profile", methods=["GET"])
def profile():
    """profile"""
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": user.email}), 200
    abort(403)


@app.route("/reset_password", methods=["POST"])
def get_reset_password_token():
    """reset password"""
    try:
        email = request.form["email"]
    except KeyError:
        abort(403)

    try:
        reset_token = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)

    return jsonify({"email": email, "reset_token": reset_token}), 200


@app.route("/reset_password", methods=["PUT"])
def update_password():
    """update password"""
    try:
        email = request.form["email"]
        reset_token = request.form["reset_token"]
        new_password = request.form["new_password"]
    except KeyError:
        abort(403)

    try:
        AUTH.update_password(reset_token, new_password)
    except ValueError:
        abort(403)

    return jsonify({"email": email, "message": "Password updated"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
