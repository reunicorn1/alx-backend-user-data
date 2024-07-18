#!/usr/bin/env python3
from flask import Flask, jsonify, request, abort, make_response, redirect
from auth import Auth


AUTH = Auth()
app = Flask(__name__)


@app.route("/", methods=["GET"])
def main() -> str:
    """The main route of the application
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def users() -> str:
    """This route registersa a user to the server
    """
    email = request.form["email"]
    password = request.form["password"]
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": f"{email}", "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login() -> str:
    """This route registers a user and gives him a session_id
    """
    email, password = request.form["email"], request.form["password"]
    if AUTH.valid_login(email, password):
        session = AUTH.create_session(email)
        resp = make_response({"email": f"{email}", "message": "logged in"})
        resp.set_cookie("session_id", session)
        return resp
    else:
        abort(401)


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout() -> str:
    """This route destroys a session with a linked user
    """
    session = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session)
    if user:
        AUTH.destroy_session(user.id)
        return redirect("/")
    else:
        abort(403)


@app.route("/profile", methods=["GET"], strict_slashes=False)
def profile() -> str:
    """This route responsd with data about the user who hold the
    current session
    """
    session = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session)
    if user:
        return jsonify({"email": f"{user.email}"}), 200
    else:
        abort(403)


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token() -> str:
    """This route resets the password for a user
    """
    email = request.form["email"]
    try:
        token = AUTH.get_reset_password_token(email)
        return jsonify({"email": f"{email}", "reset_token": f"{token}"}), 200
    except ValueError:
        abort(403)


@app.route("/reset_password", methods=["PUT"], strict_slashes=False)
def update_password() -> str:
    """This route updates your passwords after you request a reset token
    """
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")
    try:
        AUTH.update_password(reset_token, new_password)
    except ValueError:
        abort(403)
    return jsonify({"email": email, "message": "Password updated"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
