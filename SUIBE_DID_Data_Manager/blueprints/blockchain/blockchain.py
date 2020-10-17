# -*- coding: utf-8 -*-
"""User views."""
from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required

from SUIBE_DID_Data_Manager.weidentity.weidentityClient import weidentityClient
from SUIBE_DID_Data_Manager.config import Config
from SUIBE_DID_Data_Manager.weidentity.localweid import Hash, base64_decode, base64_encode, generate_addr, ecdsa_sign
from SUIBE_DID_Data_Manager.blueprints.blockchain.models import CredentialPojo
from SUIBE_DID_Data_Manager.blueprints.did_engine.models import DID
from SUIBE_DID_Data_Manager.extensions import db, csrf_protect

import random
import time

blockchain = Blueprint('blockchain', __name__)

@blockchain.route("/register_did/<string:privkey>")
@login_required
def register_did(privkey):
    weidentity = weidentityClient(Config.get("SERVER_WEID_URL"))
    if privkey[:2] == "0x":
        account = generate_addr(priv=privkey[2:])
    else:
        account = generate_addr(priv=hex(int(privkey))[2:])
    publicKey = str(int(account["payload"]["pubv"], 16))
    nonce = str(random.randint(1, 999999999999999999999999999999))
    respBody = weidentity.create_weidentity_did_first(publicKey, nonce)

    ################ 签名过程 ##################
    signedMessage = ecdsa_sign(respBody['respBody']['encodedTransaction'], privkey)
    ###########################################

    weid_second = weidentity.create_weidentity_did_second(nonce, data=respBody['respBody']['data'],
                                                    signedMessage=signedMessage)
    return jsonify(weid_second)


@csrf_protect.exempt
@blockchain.route("/register_authority_issuer/<string:privkey>", methods=["GET", "POST"])
@login_required
def register_authority_issuer(privkey):
    weId = request.args.values("weId", None)
    if weId is None:
        return jsonify({"result": "please input weId. need args [weid, name]"})

    name = request.args.values("name", None)
    if name is None:
        return jsonify({"result": "please input name. need args [weid, name]"})
    nonce = str(random.randint(1, 9999999999999999999999999999999))
    weidentity = weidentityClient(Config.get("SERVER_WEID_URL"))

    respBody = weidentity.register_authority_issuer_first(name, weId, nonce)

    ################ 签名过程 ##################
    signedMessage = ecdsa_sign(respBody['respBody']['encodedTransaction'], privkey)
    ###########################################

    weid_second = weidentity.register_authority_issuer_second(nonce, data=respBody['respBody']['data'],
                                                    signedMessage=signedMessage)
    return jsonify(weid_second)


@csrf_protect.exempt
@blockchain.route("/register_cpt/<string:privkey>", methods=["POST"])
@login_required
def register_cpt(privkey):
    weId = request.args.values("weId", None)
    if weId is None:
        return jsonify({"result": "please input weId. need args [weid, cptJsonSchema, cptSignature]"})

    cptJsonSchema = request.args.values("cptJsonSchema", None)
    if cptJsonSchema is None:
        return jsonify({"result": "please input cptJsonSchema. need args [weId, cptJsonSchema, cptSignature]"})

    cptSignature = request.args.values("cptSignature", None)
    if cptSignature is None:
        return jsonify({"result": "please input cptSignature. need args [weId, cptJsonSchema, cptSignature]"})


    nonce = str(random.randint(1, 9999999999999999999999999999999))
    weidentity = weidentityClient(Config.get("SERVER_WEID_URL"))

    respBody = weidentity.create_cpt_first(weId, cptJsonSchema, cptSignature, nonce)


    ################ 签名过程 ##################
    signedMessage = ecdsa_sign(respBody['respBody']['encodedTransaction'], privkey)
    ###########################################


    weid_second = weidentity.create_cpt_second(nonce, data=respBody['respBody']['data'],
                                                    signedMessage=signedMessage)
    return jsonify(weid_second)


@csrf_protect.exempt
@blockchain.route("/load_credential_pojo/", methods=["POST"])
def load_credential_pojo():
    """
    导入credential pojo
    :return:
    """
    data_msg = request.get_json()
    if data_msg is None:
        return jsonify({"result": "load credential pojo failed!", "code": "400"}), 400
    claim = data_msg["result"]["claim"]
    claim_id = data_msg["result"]["claim"]["weid"]
    cptId = data_msg["result"]["cptId"]
    expirationDate = data_msg["result"]["expirationDate"]
    credentialID = data_msg["result"]["id"]
    issuer = data_msg["result"]["issuer"]
    issuanceDate = data_msg["result"]["issuanceDate"]
    proof = data_msg["result"]["proof"]
    type = data_msg["result"]["type"]
    try:
        if not DID.query.filter_by(did=claim_id).first():
            return jsonify({"result": "We don't have this chaim ID locally", "code": "400"}), 400
        if claim_id == issuer:
            return jsonify({"result": "The publisher cannot be the same person as the witness.", "code": "400"}), 400
        if CredentialPojo.query.filter_by(credentialID=credentialID).first():
            return jsonify({"result": "this credentialID already have, please change this id.", "code": "400"}), 400

        credential_pojo = CredentialPojo(credentialID=credentialID, cptId=cptId, claim=claim, claim_id=claim_id,
                                         expirationDate=expirationDate, issuer_id=issuer, issuanceDate=issuanceDate,
                                         proof=proof, type=type)
        update_did = DID.query.filter_by(did=claim_id).first()
        # 添加did的链接
        update_did.credential_pojo.append(credential_pojo)
        db.session.add(credential_pojo)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            db.session.commit()
        return jsonify({"result": "load credential pojo success!", "code": "200", "data": data_msg})
    except Exception as e:
        return jsonify({"result": "load credential pojo failed!", "errorMessage":e, "code": "400"}), 400


@blockchain.route("/get_credential_pojo_by_claim_id/<string:claim_id>")
def get_credential_pojo_by_claim_id(claim_id):
    """
    获取本地数据库存储的credential pojo信息
    :param cptId: 通过cpt指定credential pojo
    :return:
    """
    credentials_pojo = CredentialPojo.query.filter_by(claim_id=claim_id).all()
    credential_pojo_all = {"result": [], "total": ""}
    for credential_pojo in credentials_pojo:
        credential_pojo_dict = {}
        credential_pojo_dict["credentialID"] = credential_pojo.credentialID
        credential_pojo_dict["issuanceDate"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.localtime(credential_pojo.issuanceDate))
        credential_pojo_dict["type"] = credential_pojo.type
        if credential_pojo.is_cochain:
            credential_pojo_dict["is_cochain"] = "已上链"
        else:
            credential_pojo_dict["is_cochain"] = "未上链"
        credential_pojo_all["result"].append(credential_pojo_dict)
    credential_pojo_all["total"] = str(len(credentials_pojo))
    return jsonify(credential_pojo_all)

@blockchain.route("/get_credential_pojo_by_credential_id/<string:credentialID>")
def get_credential_pojo_by_credential_id(credentialID):
    """
    获取本地数据库存储的credential pojo信息
    :param cptId: 通过cpt指定credential pojo
    :return:
    """
    credential_pojo = CredentialPojo.query.filter_by(credentialID=credentialID).first()
    if credential_pojo is None:
        return jsonify({"errorMessage": "We didn't find the specific information through this ID, Please enter the correct credentialID.", "code": "400"}), 400
    credential_pojo_dict = {}
    credential_pojo_dict["credentialID"] = credential_pojo.credentialID
    credential_pojo_dict["claim"] = credential_pojo.claim
    credential_pojo_dict["issuer"] = credential_pojo.issuer_id
    credential_pojo_dict["issuanceDate"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.localtime(credential_pojo.issuanceDate))
    credential_pojo_dict["cptId"] = credential_pojo.cptId
    credential_pojo_dict["expirationDate"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.localtime(credential_pojo.expirationDate))

    credential_pojo_dict["proof"] = credential_pojo.proof
    credential_pojo_dict["type"] = credential_pojo.type
    # credential_pojo_dict["is_cochain"] = credential_pojo.is_cochain
    if credential_pojo.is_cochain:
        credential_pojo_dict["is_cochain"] = "已上链"
    else:
        credential_pojo_dict["is_cochain"] = "未上链"
    return jsonify({"result": credential_pojo_dict})


@blockchain.route("/create_credential_pojo/<string:credentialID>")
@login_required
def create_credential_pojo(credentialID):
    """
    将本地credential pojo上链
    :param cptId:
    :return:
    """
    credential_pojo = CredentialPojo.query.filter_by(credentialID=credentialID).first()
    weidentity = weidentityClient(Config.get("SERVER_WEID_URL"))
    result_all = {"result": []}

    respBody = weidentity.create_credential_pojo(cptId=credential_pojo.cptId, issuer_weid=credential_pojo.issuer_id,
                                                 expirationDate=credential_pojo.expirationDate,
                                                 claim=credential_pojo.claim)

    credential_pojo.is_cochain = True
    result_all["result"].append(respBody)
    db.session.commit()
    return jsonify(result_all)


@blockchain.route("/delete_local_credential_pojo/<string:credentialID>", methods=["GET", "POST"])
def delete_local_credential_pojo(credentialID):
    credential_pojo = CredentialPojo.query.filter_by(credentialID=credentialID).first()
    if credential_pojo:
        db.session.delete(credential_pojo)
        db.session.commit()
        return jsonify({"result": "{} successfully deleted!".format(credentialID), "code": "200"})
    return jsonify({"result": "We did not find the certificate or the certificate is linked.", "code": "400"}), 400


@blockchain.route("/uplink_credential/<string:credentialID>", methods=["POST"])
def uplink_credential(credentialID):
    credential_pojo = CredentialPojo.query.filter_by(credentialID=credentialID).first()
    if credential_pojo:
        credential_pojo.is_cochain = True
        db.session.commit()
        return jsonify({"result": "{} successfully uplink!".format(credentialID), "code": "200"})
    return jsonify({"result": "We did not find the certificate.", "code": "400"}), 400
