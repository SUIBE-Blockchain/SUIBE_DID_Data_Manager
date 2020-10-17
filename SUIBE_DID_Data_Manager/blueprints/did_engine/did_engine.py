from flask import render_template, request, flash, redirect, url_for,  jsonify, Blueprint
from flask_login import login_required, current_user, login_user, logout_user

from SUIBE_DID_Data_Manager.weidentity.localweid import generate_addr, create_privkey, base64_decode, base64_encode, Hash
from SUIBE_DID_Data_Manager.weidentity.weidentityClient import weidentityClient
from SUIBE_DID_Data_Manager.weidentity.weidentityService import weidentityService
from SUIBE_DID_Data_Manager.blueprints.did_engine.models import DID
from SUIBE_DID_Data_Manager.extensions import db
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
    else:
        if privkey[:2] == "0x":
            account = generate_addr(priv=privkey[2:])
        else:
            account = generate_addr(priv=hex(int(privkey))[2:])

    addr = account["payload"]["addr"]
    # 拼接weid，这里CHAIN_ID是留给上链用的。
    weid = "did:weid:CHAIN_ID:{addr}".format(addr=addr)
    data = {
        "data": {
            "errorCode": 0,
            "errorMessage": "success",
            "privateKeyHex": account["payload"]["priv"],
            "publicKeyHex": account["payload"]["pubv"],
            "privateKeyInt": str(int(account["payload"]["priv"], 16)),
            "publicKeyInt": str(int(account["payload"]["pubv"], 16)),
            "weId": weid,
        }
    }
    weid = DID(username=current_user.username, did=weid, type="weid", privkey_hex=account["payload"]["priv"],
               privkey_int=str(int(account["payload"]["priv"], 16)),
                publickey_hex=account["payload"]["pubv"],
                publickey_int=str(int(account["payload"]["pubv"], 16)))
    db.session.add(weid)
    db.session.commit()
    return jsonify(data)


@did_engine.route("/create_weid_server")
def create_weid_server():
    weid = weidentityService(Config.get("LOCAL_WEID_URL"))
    weid_result = weid.create_weidentity_did()
    item = weid_result["respBody"].split(":")
    item[2] = "CHAIN_ID"
    weid_return = ":".join(item)
    weid = DID(username=current_user.username, did=weid_return, type="weid")
    db.session.add(weid)
    db.session.commit()
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


@did_engine.route("/did_doc")
def did_doc():
    weid = request.args.get("weid")
    if not weid:
        raise TypeError("weid can not be None.")
    weidentity = weidentityService(Config.get("SERVER_WEID_URL"))
    weid_result = weidentity.get_weidentity_did(weid)
    return jsonify({"data": weid_result})


@did_engine.route("/get_did_doc_by_weid_view")
def get_did_doc_by_weid_view():
    weid = request.args.get("weid")
    if not weid:
        return jsonify({"result": "can not found weid."})
    data_dict = {
      "data": {
        "errorCode": 0,
        "errorMessage": "success",
        "respBody": {
          "@context": "https://github.com/WeBankFinTech/WeIdentity/blob/master/context/v1",
          "authentication": [
            {
              "publicKey": "did:weid:1:0x0c8a7279207606838b16053cd526fd49c6c560c0#keys-0",
              "revoked": "false",
              "type": "Secp256k1"
            }
          ],
          "created": 1601910139,
          "id": weid,
          "publicKey": [
            {
              "id": "{weid}#keys-0".format(weid=weid),
              "owner": weid,
              "publicKey": "1HaqOCf1kgOvAzBeZdOoFp/G+Rl53nsqt28L5IcRnGotuExd4//+N7sHI6yUks2r4iH9yqXnpbEK6ZgvPtkA8Q==",
              "revoked": "false",
              "type": "Secp256k1"
            }
          ],
          "service": [],
          "updated": "null"
        }
      }
    }
    return jsonify(data_dict)

@did_engine.route("/inttohex")
def inttohex():
    int_data = request.args.get("intdata")
    hex_data = hex(int(int_data))
    return jsonify({"intData": int_data, "hexData": hex_data})

@did_engine.route("/hextoint")
def hextoint():
    hex_data = request.args.get("hexdata")
    int_data = int(hex_data, 16)
    return jsonify({"intData": int_data, "hexData": hex_data})