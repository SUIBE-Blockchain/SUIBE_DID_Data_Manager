from flask import render_template, request, flash, redirect, url_for,  jsonify, Blueprint
from flask_login import login_required, current_user, login_user, logout_user

import os

api_v1 = Blueprint('api_v1', __name__)
