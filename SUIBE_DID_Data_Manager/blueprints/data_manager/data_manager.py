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

