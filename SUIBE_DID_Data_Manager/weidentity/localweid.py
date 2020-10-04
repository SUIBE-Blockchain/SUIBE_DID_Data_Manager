# -*- coding:utf8 -*-
import os

from eth_account import Account
import sha3
import base64
import hashlib
from ecdsa import SigningKey, SECP256k1
def create_privkey():
    return os.urandom(32)

def create_ecdsa_privkey():
    return SigningKey.generate(curve=SECP256k1)

class ECDSA():
    def __init__(self):

        self.private_key = SigningKey.generate(curve=SECP256k1)
        # self.private_key = self.private_key.to_string()
        self.public_key = self.private_key.get_verifying_key()
    def Sign(self, message):
        if isinstance(message, str):
            message = bytes(message, 'utf-8')
        return self.private_key.sign(message, hashfunc=hashlib.sha256)
    def Verify(self, signature, message):
        if isinstance(message, str):
            message = bytes(message, 'utf-8')
        return self.public_key.verify(signature, message)


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