# -*- coding: utf-8 -*-
"""User views."""
from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required

from SUIBE_DID_Data_Manager.weidentity.weidentityClient import weidentityClient
from SUIBE_DID_Data_Manager.config import Config
from SUIBE_DID_Data_Manager.weidentity.localweid import Hash, base64_decode, base64_encode, generate_addr

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