# -*- coding: utf-8 -*-
"""User views."""
from flask import Blueprint, render_template, jsonify, request, g
from flask_login import login_required, current_user
import os
from SUIBE_DID_Data_Manager.weidentity.localweid import create_weid_by_privkey, create_random_weid, verify_did, update_did_chain_id
from SUIBE_DID_Data_Manager.extensions import db, csrf_protect
from SUIBE_DID_Data_Manager.blueprints.did_engine.models import DID
import time

auth_manager = Blueprint('auth_manager', __name__)

@auth_manager.route("/import_did/<string:privkey>")
def import_did(privkey):
    # chain_id = request.args.get("chain_id", "CHAIN_ID")
    # chain_name = request.args.get("chain_name")
    if not privkey:
        return jsonify({"result": "请提供正确的privkey。"})
    data_msg = create_weid_by_privkey(privkey, chain_id="CHAIN_ID")
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
               created_at=time.time(),
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
        did_dict["chain_id"] = did.chain_id
        did_dict["chain_name"] = did.chain_name
        # did_dict["is_cochain"] = did.is_cochain
        if did.is_cochain:
            did_dict["is_cochain"] = "已上链"
        else:
            did_dict["is_cochain"] = "未上链"
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
    did_all = {"result": [], "total_did": ""}
    dids = DID.query.filter_by(username=current_user.username).all()
    if not dids:
        return jsonify({"result": "We did not find did content under this user", "code":"400"}), 400

    total_did = 0
    for did in dids:
        if did.is_cochain:
            # 判断是否上链，返回上链了的数据
            total_did=total_did+1
            did_dict = {}
            did_dict["chain_name"] = did.chain_name
            did_dict["credential"] = {}
            total_credential = 0
            did_dict["credential"]["credential_cpt_type"] = []
            for credential in did.credential_pojo:
                did_dict["credential"]["credential_cpt_type"].append(str(credential.type))
                total_credential += 1
            did_dict["credential"]["total_credential"] = str(total_credential)
            did_all["result"].append(did_dict)
    did_all["total_did"] = str(total_did)
    return jsonify(did_all)


@csrf_protect.exempt
@auth_manager.route("/delete_did/<string:weid>", methods=["POST"])
def delete_did(weid):
    did = DID.query.filter_by(did=weid).first()
    if did:
        db.session.delete(did)
        db.session.commit()
        return jsonify({"result": "{} successfully deleted!".format(did.did), "code": "200"})
    return jsonify({"result": "We did not find the did", "code": "400"}), 400

@csrf_protect.exempt
@auth_manager.route("/uplink_did/<string:weid>", methods=["POST"])
def uplink_did(weid):
    data_msg = request.get_json()
    chain_id = data_msg.get("chain_id", None)
    chain_name = data_msg.get("chain_name", None)
    if not chain_id or not chain_name:
        return jsonify({"result": "Please enter chain ID and chain name.[chain_id, chain_name]", "code": "400"}), 400

    did = DID.query.filter_by(did=weid, is_cochain=False).first()
    if did:
        did.did = update_did_chain_id(did.did, chain_id)
        did.is_cochain = True
        did.chain_id = chain_id
        did.chain_name = chain_name
        did.uplinked_at = time.time()
        db.session.commit()
        return jsonify({"result": "{} successfully uplink!".format(did.did), "code": "200"})
    return jsonify({"result": "We did not find the did or already uplinked.", "code": "400"}), 400
