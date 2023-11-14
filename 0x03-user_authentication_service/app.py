#!/usr/bin/env python3
"""A basic flask app"""
from flask import Flask, jsonify, redirect, request, abort
from auth import Auth

app = Flask(__name__)
Auth = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def index():
    """A basic flask application that returns JSON"""
    return jsonify({"message": "Nienvenue"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
