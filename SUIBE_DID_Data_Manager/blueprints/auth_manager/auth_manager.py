# -*- coding: utf-8 -*-
"""User views."""
from flask import Blueprint, render_template, jsonify, request, g
from flask_login import login_required
import os
from SUIBE_DID_Data_Manager.weidentity.localweid import create_weid_by_privkey, create_random_weid, verify_did

auth_manager = Blueprint('auth_manager', __name__)


@auth_manager.route("/import_did/<string:privkey>")
def import_did(privkey):
    chain_id = request.args.get("chain_id", "CHAIN_ID")
    if not privkey:
        return jsonify({"result": "请提供正确的privkey。"})
    data_msg = create_weid_by_privkey(privkey, chain_id)
    data_dict = {
        "data": {
            "privateKeyHex": data_msg["privateKeyHex"],
            "privateKeyInt": data_msg["privateKeyInt"],
            "publicKeyHex": data_msg["publicKeyHex"],
            "publicKeyInt": data_msg["publicKeyInt"],
            "weId": data_msg["weid"],
            "transactionInfo": {
                "blockNumber": 32220,
                "transactionHash": os.urandom(32).hex(),
                "transactionIndex": 0
                }
            }
        }
    return data_dict

@auth_manager.route("/export_did/<string:weId>")
def export_did(weId):
    verify_data = verify_did(weId)
    if verify_data != True:
        return jsonify({"errorMessage": verify_data})
    random_msg = create_random_weid()

    data_dict = {
        "errorMessage": "success",
        "data": {
            "privateKeyHex": random_msg["privateKeyHex"],
            "privateKeyInt": random_msg["privateKeyInt"],
            "publicKeyHex": random_msg["publicKeyHex"],
            "publicKeyInt": random_msg["publicKeyInt"],
            "weId": weId
        }
    }
    return data_dict
