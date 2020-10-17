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
    did_all = {"result": [], "total": ""}
    for did in dids:
        did_dict = {}
        did_dict["username"] = did.username
        did_dict["did"] = did.did
        did_dict["type"] = did.type
        did_dict["is_cochain"] = did.is_cochain
        if did.privkey_int:
            did_dict["privkey_int"] = did.privkey_int
            did_dict["privkey_hex"] = did.privkey_hex
        if did.publickey_int:
            did_dict["publickey_int"] = did.publickey_int
            did_dict["publickey_hex"] = did.publickey_hex
        did_all["result"].append(did_dict)
    did_all["total"] = str(len(dids))
    return jsonify(did_all)

@auth_manager.route("/auth_tree/")
@login_required
def auth_tree():
    return_message = []
    did_all = {"result": [], "total_did": ""}
    dids = DID.query.filter_by(username=current_user.username).all()
    if not dids:
        return jsonify({"result": "We did not find did content under this user", "code":"400"}), 400

    total_did = len(dids)
    for did in dids:
        did_dict = {}
        did_dict[did.did] = {}
        total_credential = 0

        did_dict[did.did]["credential_cptid"] = []
        for credential in did.credential_pojo:
            did_dict[did.did]["credential_cpt_type"].append(str(credential.type))
            total_credential += 1
        did_dict[did.did]["total_credential"] = str(total_credential)
        did_all["result"].append(did_dict)
    did_all["total_did"] = str(total_did)
    return jsonify(did_all)

