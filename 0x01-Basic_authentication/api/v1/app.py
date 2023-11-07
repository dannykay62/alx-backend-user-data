from flask import Flask, request
from os import getenv

app = Flask(__name__)

@app.route('/')
def index():
    return "OK"

if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)