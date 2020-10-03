from flask import render_template, request, flash, redirect, url_for,  jsonify, Blueprint
from flask_login import login_required, current_user, login_user, logout_user

from SUIBE_DID_Data_Manager.weidentity.localweid import generate_addr, create_privkey, base64_decode, base64_encode, Hash
from SUIBE_DID_Data_Manager.weidentity.weidentityClient import weidentityClient
from SUIBE_DID_Data_Manager.weidentity.weidentityService import weidentityService
from SUIBE_DID_Data_Manager.config import Config

import random
from ecdsa import SigningKey, SECP256k1
from pprint import pprint

did_engine = Blueprint('did_engine', __name__)


@did_engine.route("/create_weid_local_func")
@login_required
def create_weid_local_func():
    # 通过get的方式传送一个privkey data。
    privkey = request.args.get("privkey", None)
    if privkey == None:
        privkey = create_privkey()
    account = generate_addr(priv=privkey.hex())
    addr = account["payload"]["addr"]
    # 拼接weid，这里CHAIN_ID是留给上链用的。
    weid = "did:weid:CHAIN_ID:{addr}".format(addr=addr)
    data = {
        "weid": {
            "errorCode": 0,
            "errorMessage": "success",
            "privateKey ": account["payload"]["priv"],
            "publicKey": account["payload"]["pubv"],
            "respBody": weid,
        }
    }
    return jsonify(data)


@did_engine.route("/create_weid_server")
def create_weid_server():
    weid = weidentityService(Config.get("LOCAL_WEID_URL"))
    weid_result = weid.create_weidentity_did()
    item = weid_result["respBody"].split(":")
    item[2] = "CHAIN_ID"
    weid_return = ":".join(item)
    return jsonify({"weid": weid_return})


@did_engine.route("/create_weid_local_server")
def create_weid_local_server():
    """
    TODO: 签名存在问题
    :return:
    """
    weid = weidentityClient(Config.get("LOCAL_WEID_URL"))
    # 创建私钥
    signning_key = SigningKey.generate(curve=SECP256k1)
    privkey = signning_key.to_string()
    # 创建公钥
    verifing_key = signning_key.get_verifying_key()
    publicKey = str(eval("0x" + verifing_key.to_string().hex()))

    # 获取 nonce
    nonce = str(random.randint(1, 999999999999999999999999999999))
    respBody = weid.create_weidentity_did_first(publicKey, nonce)
    encode_transaction = respBody['respBody']['encodedTransaction']
    # base64解密
    transaction = base64_decode(encode_transaction)
    # 计算hash
    hashedMsg = Hash(transaction)
    # 签名
    signature = signning_key.sign(bytes(hashedMsg, "utf-8"))
    # base加密
    transaction_encode = base64_encode(signature)
    weid_second = weid.create_weidentity_did_second(nonce, data=respBody['respBody']['data'],
                                                    signedMessage=transaction_encode)
    pprint(weid_second)
    data = {
        "weid": weid_second
    }
    return jsonify(data)