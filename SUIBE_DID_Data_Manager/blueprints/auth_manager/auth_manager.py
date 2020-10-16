# -*- coding: utf-8 -*-
"""User views."""
from flask import Blueprint, render_template, jsonify, request, g
from flask_login import login_required, current_user
import os
from SUIBE_DID_Data_Manager.weidentity.localweid import create_weid_by_privkey, create_random_weid, verify_did
from SUIBE_DID_Data_Manager.extensions import db
from SUIBE_DID_Data_Manager.blueprints.did_engine.models import DID

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
    weid = DID(username=current_user.username,
               did=data_msg["weid"], type="weid",
               privkey_hex=data_msg["privateKeyHex"],
               privkey_int=data_msg["privateKeyInt"],
               publickey_hex=data_msg["publicKeyHex"],
               publickey_int=data_msg["publicKeyInt"])
    db.session.add(weid)
    db.session.commit()
    return data_dict

@auth_manager.route("/export_did/<string:weId>")
def export_did(weId):
    verify_data = verify_did(weId)
    if verify_data != True:
        return jsonify({"errorMessage": verify_data})
    dids = DID.query.filter_by(did=weId).all()
    did_all = []
    for did in dids:
        did_dict = {}
        did_dict["username"] = did.username
        did_dict["did"] = did.did
        did_dict["type"] = did.type
        if did.privkey_int:
            did_dict["privkey_int"] = did.privkey_int
            did_dict["privkey_hex"] = did.privkey_hex
        if did.publickey_int:
            did_dict["publickey_int"] = did.publickey_int
            did_dict["publickey_hex"] = did.publickey_hex
        did_all.append(did_dict)
    return jsonify({"data": did_all})

@auth_manager.route("/get_user_did/")
@login_required
def get_user_did():
    dids = DID.query.filter_by(username=current_user.username).all()
    did_all = []
    for did in dids:
        try:
            print(did.credential_pojo[0].proof)
        except Exception as e:
            print(e)
        did_dict = {}
        did_dict["username"] = did.username
        did_dict["did"] = did.did
        did_dict["type"] = did.type
        if did.privkey_int:
            did_dict["privkey_int"] = did.privkey_int
            did_dict["privkey_hex"] = did.privkey_hex
        if did.publickey_int:
            did_dict["publickey_int"] = did.publickey_int
            did_dict["publickey_hex"] = did.publickey_hex
        did_all.append(did_dict)
    return jsonify({"data": did_all})