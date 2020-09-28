from flask import render_template, request, flash, redirect, url_for,  jsonify, Blueprint
from flask_login import login_required, current_user, login_user, logout_user

import os
from SUIBE_DID_Data_Manager.weidentity.localweid import generate_addr, create_privkey
from SUIBE_DID_Data_Manager.weidentity.weidentityClient import weidentityClient
from SUIBE_DID_Data_Manager.weidentity.weidentityService import weidentityService
from SUIBE_DID_Data_Manager.config import Config
import random

api_v1 = Blueprint('api_v1', __name__)


@api_v1.route("/create_weid_local_func")
@login_required
def create_weid_local_func():
    # 创建私钥，这里是mock data，TODO: 需要实现生成唯一的，随机的64位的私钥
    privkey = request.args.get("privkey", None)
    account = generate_addr(priv=privkey)
    addr = account["payload"]["addr"]
    # 拼接weid，这里CHAIN_ID是留给上链用的。
    weid = "did:weid:CHAIN_ID:{addr}".format(addr=addr)
    data = {
        "weid": {
            "errorCode": 0,
            "errorMessage": "success",
            # "privateKey ": account["payload"]["priv"],
            "publicKey": account["payload"]["pubv"],
            "respBody": weid,
        }
    }
    return jsonify(data)

@api_v1.route("/create_weid_local_server")
def create_weid_local_server():
    local_server_url = Config.get("LOCAL_WEID_URL")
    weclient = weidentityClient(local_server_url)
    weserver = weidentityService(local_server_url)
    # publicKey 是1-154位的10进制data
    publicKey = str(random.randint(1, 9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999))
    nonce = str(random.randint(1, 999999999999999999999999999999))
    weid_first = weclient.create_weidentity_did_first(publicKey, nonce)
    print(weid_first)
    weid_second = weclient.create_weidentity_did_second(nonce, data="1131231", signedMessage="1231321")
    print(weid_second)
    # 利用server 的api 创建weid，这里缺少 客户端api 两次调用的案例。
    # weid = weserver.create_weidentity_did()

    data = {
        "weid": weid_second
    }
    return jsonify(data)
