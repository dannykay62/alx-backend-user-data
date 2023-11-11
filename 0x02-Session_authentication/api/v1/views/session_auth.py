#!/usr/bin/env python3
""""handles all routes for the Session authentication"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
from os import getenv


@app_views.route('/auth_seesion/login', methods=['POST'], strict_slashes=False
                 )
def login() -> str:
    """app view for login route with a POST method"""
    email = request.form.get('email')
    if not email:
        return jsonify({"error": "email missing"}), 400
    password = request.form.get('password')
    if not password:
        return jsonify({"error": "password missing"}), 400
    user = User.search({'email': email})
    if not user:
        return jsonify({"error": "no user found for this email"}), 400
    for u in user:
        if u.is_valid_password(password):
            from api.v1.app import auth
            session_id = auth.create_session(u.id)
            user_json = jsonify(u.to_json())
            user_json.set_cookie(getenv('SESSION_NAME'), session_id)
            return user_json
        else:
            return jsonify({"error": "wrong password"}), 401

    @app_views.route('/auth_session/logout', methods=['DELETE'],
                     strict_slashes=False)
    def logout() -> str:
        """route for delete or logout"""
        from api.v1.app import auth
        destroy_session = auth.destroy_session(request)
        if destroy_session is False:
            abort(404)
        else:
            return jsonify({}), 200
