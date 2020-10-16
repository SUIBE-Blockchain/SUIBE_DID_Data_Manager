# -*- coding: utf-8 -*-
"""User views."""
from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required, current_user
from SUIBE_DID_Data_Manager.extensions import csrf_protect
from SUIBE_DID_Data_Manager.weidentity.localweid import create_watting_weid, create_random_weid, ecdsa_sign
from SUIBE_DID_Data_Manager.weidentity.weidentityClient import weidentityClient
from SUIBE_DID_Data_Manager.config import Config

from ecdsa import SigningKey, SECP256k1
import random

weid_api = Blueprint('weid_api', __name__)


@csrf_protect.exempt
@weid_api.route("/api/transact", methods=["POST"])
@login_required
def transact():
    data_msg = request.get_json()
    weid = create_random_weid()
    return_data = {
        "ErrorCode": 0,
        "ErrorMessage": "success",
        "respBody": weid["weId"]
    }
    return jsonify(return_data)


@csrf_protect.exempt
@weid_api.route("/api/signencode", methods=["POST"])
def signencode():
    weid = weidentityClient(Config.get("LOCAL_WEID_URL"))
    signning_key = SigningKey.generate(curve=SECP256k1)
    privkey = signning_key.to_string()
    # 创建公钥
    verifing_key = signning_key.get_verifying_key()
    publicKey = str(eval("0x" + verifing_key.to_string().hex()))
    # 获取 nonce
    nonce = str(random.randint(1, 999999999999999999999999999999))
    respBody = weid.create_weidentity_did_first(publicKey, nonce)
    encode_transaction = respBody['respBody']['encodedTransaction']
    signatureValue = ecdsa_sign(encode_transaction=encode_transaction, privkey=privkey)
    return_data = {
        "ErrorCode": 0,
        "ErrorMessage": "success",
        "signatureValue": signatureValue
    }
    return jsonify(return_data)


