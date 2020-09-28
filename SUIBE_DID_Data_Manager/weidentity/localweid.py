# -*- coding:utf8 -*-
import os

from eth_account import Account

def create_privkey():
    return os.urandom(32).hex()

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
                 "pubv": str(account._key_obj.public_key)
                 }}
# a = generate_addr()
# print(a)/