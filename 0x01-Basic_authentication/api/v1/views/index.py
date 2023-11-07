#!/usr/bin/env python3
"""Views for the index
"""
from flask import jsonify, abort
from api.v1.views import app_views


@app_views.route('/staus', methods=['GET'], strict_slashes=False)
def status() -> str:
    """GET /api/v1/status
        Return: the API status
    """
    return jsonify({"status": "ok"})


@app_views.route('/unauthorized', methods=['GET'], strict_slashes=False)
def forbidden() -> str:
    """endpoint for error handler to test (unauthorized)"""
    abort(401)
