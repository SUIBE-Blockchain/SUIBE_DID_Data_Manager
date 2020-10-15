# -*- coding:utf8 -*-
import os

from eth_account import Account
import sha3
import base64
import hashlib
from ecdsa import SigningKey, SECP256k1
DID_TYPE = ["weid"]
def create_privkey():
    return os.urandom(32)

def create_ecdsa_privkey():
    return SigningKey.generate(curve=SECP256k1)

def create_random_weid():
    # 通过get的方式传送一个privkey data。
    privkey = create_privkey()
    account = generate_addr(priv=privkey.hex())

    addr = account["payload"]["addr"]
    # 拼接weid，这里CHAIN_ID是留给上链用的。
    weid = "did:weid:CHAIN_ID:{addr}".format(addr=addr)
    data = {
        "privateKeyHex": account["payload"]["priv"],
        "publicKeyHex": account["payload"]["pubv"],
        "privateKeyInt": str(int(account["payload"]["priv"], 16)),
        "publicKeyInt": str(int(account["payload"]["pubv"], 16)),
        "weId": weid,
    }
    return data

def create_weid_by_privkey(privkey, chain_id):
    if privkey[:2] == "0x":
        account = generate_addr(priv=privkey[2:])
    else:
        account = generate_addr(priv=hex(int(privkey))[2:])

    addr = account["payload"]["addr"]
    # 拼接weid，这里CHAIN_ID是留给上链用的。
    weid = "did:weid:{chain_id}:{addr}".format(chain_id=chain_id, addr=addr)
    data = {
        "privateKeyHex": account["payload"]["priv"],
        "publicKeyHex": account["payload"]["pubv"],
        "privateKeyInt": str(int(account["payload"]["priv"], 16)),
        "publicKeyInt": str(int(account["payload"]["pubv"], 16)),
        "weid": weid,
    }
    return data

def generate_addr(priv=None):
    if priv == None:
        account = Account.create()
    else:
        try:
            account = Account.privateKeyToAccount(priv)
        except Exception as e:
            return {"result": "error", "error":e}
    return {"result": "success",
            "payload":
                {"addr": account.address,
                 "priv": account.privateKey.hex(),
                 "pubv": str(account._key_obj.public_key).lower()
                 }}


def verify_did(did):
    verify_data = did.split(":")

    if verify_data[0] != "did":
        return "请提供正确的did。"
    if verify_data[1] not in DID_TYPE:
        return "请提供正确的DID Type。"
    if verify_data[2] == "CHAIN_ID":
        return "请指定正确的chain id。"
    if verify_data[3][:2] != "0x":
        return "请输入正确的did。"
    return True

def Hash(msg):
    k = sha3.keccak_256()
    k.update(msg)
    return k.hexdigest()

def ethtype_to_int_priv_pubv(priv, pubv):
    """
    将 priv 和 pubv 转换为 weidentity 支持的格式（十进制）
    :param priv: type: bytes
    :param pubv:  type: hex
    :return: priv int, pubv int
    """
    private_key = int.from_bytes(priv, byteorder='big', signed=False)
    public_key = eval(pubv)
    return {"priv": str(private_key), "pubv": str(public_key)}

def int_to_ethtype_priv_pubv(priv, pubv):
    pass

def base64_decode(base_data):
    """
    base64解密
    :param base_data:
    :return:
    """
    bytes_data = base64.b64decode(base_data)
    return bytes_data

def base64_encode(bytes_data):
    """
    base64加密
    :param str_data:
    :return:
    """
    base_data = base64.b64encode(bytes_data)
    return bytes.decode(base_data)


def binary_to_list(bin):
    list = []
    for idx, val in enumerate(bin):
        list.append(val)
    return list


def list_to_binary(list):
    bin = b''
    for i in list:
        bin += bytes([i])
    return bin
