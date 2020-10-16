# -*- coding: utf-8 -*-
"""User views."""
from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required, current_user
from SUIBE_DID_Data_Manager.extensions import csrf_protect
from SUIBE_DID_Data_Manager.weidentity.localweid import create_watting_weid
import random

weid_api = Blueprint('weid_api', __name__)


@csrf_protect.exempt
@weid_api.route("/api/transact", methods=["POST"])
@login_required
def transact():
    data_msg = request.get_json()
    weid = ["did:weid:CHAIN_ID:0xeD908f9a9882C027686Cb79644b9D3cd94a40b0d",
            "did:weid:CHAIN_ID:0xdEd8b9537bFcB2D840DAAA378a7076310f556C1a",
            "did:weid:CHAIN_ID:0x63F02fa8b2b84Dbf496659c8C26D0158AaB38aC5",
            "did:weid:CHAIN_ID:0xc4d0F3778d7c04deA77172Bb812e0D3635FCEA8f",
            "did:weid:CHAIN_ID:0x71FB87d8AC2de0dE72E28A0d5407e216B827c5D5", ]

    weid_return = weid[random.randint(0, len(weid)-1)]

    return_data = {
        "ErrorCode": 0,
        "ErrorMessage": "success",
        "respBody": weid_return
    }

    return jsonify(return_data)
