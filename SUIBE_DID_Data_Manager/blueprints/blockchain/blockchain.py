# -*- coding: utf-8 -*-
"""User views."""
from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required

from SUIBE_DID_Data_Manager.weidentity.weidentityClient import weidentityClient
from SUIBE_DID_Data_Manager.config import Config
from SUIBE_DID_Data_Manager.weidentity.localweid import Hash, base64_decode, base64_encode, generate_addr
from SUIBE_DID_Data_Manager.blueprints.blockchain.models import CredentialPojo
from SUIBE_DID_Data_Manager.extensions import db

import random

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
    encode_transaction = respBody['respBody']['encodedTransaction']
    # base64解密
    transaction = base64_decode(encode_transaction)
    # 获取hash
    hashedMsg = Hash(transaction)
    bytes_hashed = bytes(bytearray.fromhex(hashedMsg))
    signature = signning_key.sign(bytes_hashed)
    transaction_encode = base64_encode(signature)
    ###############################################3


    weid_second = weidentity.create_weidentity_did_second(nonce, data=respBody['respBody']['data'],
                                                    signedMessage=transaction_encode)
    return jsonify(weid_second)



@blockchain.route("/register_authority_issuer/<string:weId>")
@login_required
def register_authority_issuer(weId):
    name = request.args.get("name", None)
    if name is None:
        return jsonify({"result": "please input name."})
    nonce = str(random.randint(1, 9999999999999999999999999999999))
    weidentity = weidentityClient(Config.get("SERVER_WEID_URL"))

    respBody = weidentity.register_authority_issuer_first(name, weId, nonce)


    ################ 签名过程 ##################
    encode_transaction = respBody['respBody']['encodedTransaction']
    # base64解密
    transaction = base64_decode(encode_transaction)
    # 获取hash
    hashedMsg = Hash(transaction)
    bytes_hashed = bytes(bytearray.fromhex(hashedMsg))
    signature = signning_key.sign(bytes_hashed)
    transaction_encode = base64_encode(signature)
    ###############################################3


    weid_second = weidentity.register_authority_issuer_second(nonce, data=respBody['respBody']['data'],
                                                    signedMessage=transaction_encode)
    return jsonify(weid_second)


@blockchain.route("/register_cpt/<string:weId>", methods=["GET", "POST"])
@login_required
def register_cpt(weId):
    cptJsonSchema = request.args.values("cptJsonSchema", None)
    if cptJsonSchema is None:
        return jsonify({"result": "please input cptJsonSchema. need args [cptJsonSchema, cptSignature]"})

    cptSignature = request.args.values("cptSignature", None)
    if cptSignature is None:
        return jsonify({"result": "please input cptSignature. need args [cptJsonSchema, cptSignature]"})


    nonce = str(random.randint(1, 9999999999999999999999999999999))
    weidentity = weidentityClient(Config.get("SERVER_WEID_URL"))

    respBody = weidentity.create_cpt_first(weId, cptJsonSchema, cptSignature, nonce)


    ################ 签名过程 ##################
    encode_transaction = respBody['respBody']['encodedTransaction']
    # base64解密
    transaction = base64_decode(encode_transaction)
    # 获取hash
    hashedMsg = Hash(transaction)
    bytes_hashed = bytes(bytearray.fromhex(hashedMsg))
    signature = signning_key.sign(bytes_hashed)
    transaction_encode = base64_encode(signature)
    ###############################################3


    weid_second = weidentity.create_cpt_second(nonce, data=respBody['respBody']['data'],
                                                    signedMessage=transaction_encode)
    return jsonify(weid_second)


@blockchain.route("/load_credential_pojo/", methods=["GET", "POST"])
def load_credential_pojo():
    data_msg = request.get_json()
    if data_msg is None:
        return jsonify({"result": "load credential pojo failed!", "code": "400"}), 400
    claim = data_msg["result"]["claim"]
    cptId = data_msg["result"]["cptId"]
    expirationDate = data_msg["result"]["expirationDate"]
    credentialID = data_msg["result"]["id"]
    issuer = data_msg["result"]["issuer"]
    issuanceDate = data_msg["result"]["issuanceDate"]
    proof = data_msg["result"]["proof"]
    type = data_msg["result"].get("type", [])
    try:
        credential_pojo = CredentialPojo(credentialID=credentialID, cptId=cptId, claim=claim,
                                         expirationDate=expirationDate, issuer=issuer, issuanceDate=issuanceDate,
                                         proof=proof, type=type)
        db.session.add(credential_pojo)
        db.session.commit()
        return jsonify({"result": "load credential pojo success!", "code": "200"})
    except:
        return jsonify({"result": "load credential pojo failed!", "code": "400"}), 400


@blockchain.route("/get_credential_pojo/<int:cptId>", methods=["GET", "POST"])
def get_credential_pojo(cptId):
    """
    获取本地数据库存储的credential pojo信息
    :param cptId: 通过cpt指定credential pojo
    :return:
    """
    credentials_pojo = CredentialPojo.query.filter_by(cptId=cptId).all()
    credential_pojo_all = []
    for credential_pojo in credentials_pojo:
        credential_pojo_dict = {}
        credential_pojo_dict["credentialID"] = credential_pojo.credentialID
        credential_pojo_dict["claim"] = credential_pojo.claim
        credential_pojo_dict["issuer"] = credential_pojo.issuer
        credential_pojo_dict["issuanceDate"] = credential_pojo.issuanceDate
        credential_pojo_dict["id"] = credential_pojo.id
        credential_pojo_dict["cptId"] = credential_pojo.cptId
        credential_pojo_dict["expirationDate"] = credential_pojo.expirationDate
        credential_pojo_dict["proof"] = credential_pojo.proof
        if credential_pojo.type is not None:
            credential_pojo_dict["type"] = credential_pojo.type
        credential_pojo_all.append(credential_pojo_dict)
    return jsonify({"result": credential_pojo_all})


@blockchain.route("/create_credential_pojo/<int:cptId>", methods=["GET", "POST"])
@login_required
def create_credential_pojo(cptId):
    credentials_pojo = CredentialPojo.query.filter_by(cptId=cptId).all()
    weidentity = weidentityClient(Config.get("SERVER_WEID_URL"))
    result_all = []
    for credential_pojo in credentials_pojo:
        respBody = weidentity.create_credential_pojo(cptId=cptId, issuer_weid=credential_pojo.issuer,
                                                     expirationDate=credential_pojo.expirationDate,
                                                     claim=credential_pojo.claim)
        result_all.append(respBody)
    return jsonify(result_all)
