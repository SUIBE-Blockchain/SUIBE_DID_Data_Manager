# -*- coding: utf-8 -*-
from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
    abort
)
from flask_login import login_required, login_user, logout_user, current_user

from SUIBE_DID_Data_Manager.extensions import login_manager
from SUIBE_DID_Data_Manager.blueprints.public.forms import RegisterForm, LoginForm
from SUIBE_DID_Data_Manager.blueprints.public.models import User
from SUIBE_DID_Data_Manager.utils import flash_errors, redirect_back
from SUIBE_DID_Data_Manager.extensions import db

admin_bp = Blueprint("admin", __name__, static_folder="../static")

@admin_bp.route('/')
@login_required
def index():
    if current_user.is_admin:
        users = User.query.order_by(User.created_at.desc()).all()
        return render_template('admin/admin.html', users=users)
    else:
        return abort(404)

@admin_bp.route('/addactive', methods=['GET', 'POST'])
@login_required
def addactive():
    if current_user.is_admin:
        username = request.args.get('username')
        user = User.query.filter(User.username==username).first()
        user.active = True
        db.session.commit()
        return redirect_back()
    else:
        return abort(404)
    

@admin_bp.route('/cancleactive', methods=['GET', 'POST'])
@login_required
def cancleactive():
    if current_user.is_admin:
        username = request.args.get('username')
        user = User.query.filter(User.username==username).first()
        user.active = False
        db.session.commit()
        return redirect_back()
    else:
        return abort(404)
    

@admin_bp.route('/add_all_active', methods=['GET', 'POST'])
@login_required
def add_all_active():
    if current_user.is_admin:
        users = User.query.order_by(User.created_at.desc()).all()
        for user in users:
            user.active = True
        db.session.commit()
        return redirect_back()
    else:
        return abort(404)

@admin_bp.route('/cancle_all_active', methods=['GET', 'POST'])
@login_required
def cancle_all_active():
    if current_user.is_admin:
        users = User.query.order_by(User.created_at.desc()).all()
        for user in users:
            if not user.is_admin:
                user.active = False
        db.session.commit()
        return redirect_back()
    else:
        return abort(404)