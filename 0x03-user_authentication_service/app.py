#!/usr/bin/env python3
"""A basic flask app"""
from flask import Flask, jsonify, redirect, request, abort
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def welcome():
    """A basic flask application that returns JSON"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users():
    """ the end-point to register a user"""
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"}), 200
    except Exception:
        return jsonify({"message": "email already registered"}), 400

@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """create a new session for the user, store it the session ID as a cookie
    with key "session_id" on the response and return a JSON payload of
    the form"""
    email = request.form.get('email')
    password = request.form.get('password')
    if AUTH.valid_login(email, password) is False:
        abort(401)
    session_id = AUTH.create_session(email)
    response = jsonify({'email': email, 'message': 'logged in'})
    response.set_cookie('session_id', session_id)
    return response

@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """Find the user with the requested session ID. If the user exists destroy
    the session and redirect the user to GET /. If the user does not exist,
    respond with a 403 HTTP status"""
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if session_id is None or user is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect('/')

@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile():
    """Create user profile using the session_id cookie"""
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if session_id is None or user is None:
        abort(403)
    return jsonify({"email": user.email}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
