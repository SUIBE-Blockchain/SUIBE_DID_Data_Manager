from flask import render_template, request, flash, redirect, url_for,  jsonify, Blueprint
from flask_login import login_required, current_user, login_user, logout_user

import os
from SUIBE_DID_Data_Manager.weidentity.localweid import generate_addr, create_privkey

api_v1 = Blueprint('api_v1', __name__)


@api_v1.route("/create_weid")
def create_weid():
    privkey = create_privkey()
    addr = generate_addr(priv=privkey)["payload"]["addr"]
    weid = "did:weid:CHAIN_ID:{addr}".format(addr=addr)
    data = {
        "weid": weid
    }
    return jsonify(data)
