from flask import render_template, request, flash, redirect, url_for,  jsonify, Blueprint
from flask_login import login_required, current_user, login_user, logout_user

import os
from SUIBE_DID_Data_Manager.weidentity.localweid import generate_addr, create_privkey
from SUIBE_DID_Data_Manager.weidentity.weidentityClient import weidentityClient
from SUIBE_DID_Data_Manager.weidentity.weidentityService import weidentityService
from SUIBE_DID_Data_Manager.config import Config

api_v1 = Blueprint('api_v1', __name__)


@api_v1.route("/create_weid_local_func")
def create_weid_local_func():
    # 创建私钥，这里是mock data，TODO: 需要实现生成唯一的，随机的64位的私钥
    privkey = create_privkey()
    # 根据私钥生成地址
    addr = generate_addr(priv=privkey)["payload"]["addr"]
    # 拼接weid，这里CHAIN_ID是留给上链用的。
    weid = "did:weid:CHAIN_ID:{addr}".format(addr=addr)
    data = {
        "weid": {
            "errorCode": 0,
            "errorMessage": "success",
            "respBody": weid
        }
    }
    return jsonify(data)

@api_v1.route("/create_weid_local_server")
def create_weid_local_server():
    local_server_url = Config.get("LOCAL_WEID_URL")
    weclient = weidentityClient(local_server_url)
    weserver = weidentityService(local_server_url)
    # weid_first = weclient.create_weidentity_did_first(publicKey="91f8a28da8737b389111faeaa17143830f28d1565c1a785f27d72623f6d8f631",nonce="111faeaa1714383")
    # weid_second = weclient.create_weidentity_did_second()
    # 利用server 的api 创建weid，这里缺少 客户端api 两次调用的案例。
    weid = weserver.create_weidentity_did()

    data = {
        "weid": weid
    }
    return jsonify(data)
