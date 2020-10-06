# -*- coding: utf-8 -*-
"""User views."""
from flask import Blueprint, render_template, jsonify, request, g
from flask_login import login_required
import os
from SUIBE_DID_Data_Manager.weidentity.localweid import create_weid_by_privkey, create_random_weid, verify_did

auth_manager = Blueprint('auth_manager', __name__)


@auth_manager.route("/import_did/<string:privkey>")
def import_did(privkey):
    if not privkey:
        return jsonify({"result": "请提供正确的privkey。"})
    data_dict = {
        "data": {
            "privateKeyHex": "0x0d8584c8d14218a008e60cfc81c57c121f91e4ad1d9b4e981f53fa4cf96a6766",
            "privateKeyInt": "6115974135742557304227478679847126231241577910300293751879854207106787469158",
            "publicKeyHex": "0xf3d8e2bc7aade12be1df33caf3567a96ccf7cbaf9c0bd7b84090ea5d9b2a95a586c33475ac2c133a39f9be3fb3531728b88216fc9255e98c97fd377e67234fd5",
            "publicKeyInt": "12771314656975642938381316680267382756889741313031741595797007421451711110903116768342425935879884507205894934497572255382985758687808390989495664625536981",
            "weId": "did:weid:1:0x0c8a7279207606838b16053cd526fd49c6c560c0",
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
