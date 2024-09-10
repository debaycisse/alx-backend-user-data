#!/usr/bin/env python3
"""This module houses the implementation of a flask application"""
from flask import Flask, jsonify


app = Flask(__name__)


@app.route('/', methods=['GET'])
def entry_point():
    """Serves the entry point of the program"""
    return jsonify({"message": "Bienvenue"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
