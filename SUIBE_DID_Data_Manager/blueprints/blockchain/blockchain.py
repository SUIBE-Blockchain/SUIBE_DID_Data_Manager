# -*- coding: utf-8 -*-
"""User views."""
from flask import Blueprint, render_template, jsonify
from flask_login import login_required

blockchain = Blueprint('blockchain', __name__)

@blockchain.route("/")
@login_required
def members():
    """List members."""
    return jsonify({"result": "test"})

@blockchain.route("/input_data")
@login_required
def input_data():
    return jsonify({"result": "input_data"})
