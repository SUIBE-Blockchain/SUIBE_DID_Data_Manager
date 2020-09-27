# -*- coding:utf8 -*-
from web3 import Web3
from eth_account import Account

def create_privkey(params=None):
    return "91f8a28da8737b389111faeaa17143830f28d1565c1a785f27d72623f6d8f631"

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

# b = generate_addr(priv="91f8a28da8737b389111faeaa17143830f28d1565c1a785f27d72623f6d8f631")
# print(b)
# print(len("91f8a28da8737b389111faeaa17143830f28d1565c1a785f27d72623f6d8f631"))
# print(len("f28d1565c1a785f27d72623f6d8f6313"))