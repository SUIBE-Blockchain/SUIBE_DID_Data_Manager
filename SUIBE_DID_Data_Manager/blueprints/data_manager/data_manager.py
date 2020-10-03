# -*- coding: utf-8 -*-
"""User views."""
from flask import Blueprint, render_template, jsonify
from flask_login import login_required

data_manager = Blueprint('data_manager', __name__)

@data_manager.route("/")
@login_required
def members():
    """List members."""
    return jsonify({"result": "test"})

@data_manager.route("/input_data")
@login_required
def input_data():
    return jsonify({"result": "input_data"})
