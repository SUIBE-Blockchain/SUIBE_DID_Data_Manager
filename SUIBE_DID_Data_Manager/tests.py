from SUIBE_DID_Data_Manager.weidentity.weidentityClient import weidentityClient
from SUIBE_DID_Data_Manager.weidentity.weidentityService import weidentityService
from SUIBE_DID_Data_Manager.config import Config

import random
from ecdsa import SigningKey, SECP256k1
from eth_account import Account

from pprint import pprint
from SUIBE_DID_Data_Manager.weidentity.localweid import base64_decode, base64_encode, Hash
import time

weid = weidentityClient(Config.get("LOCAL_WEID_URL"))
cptId = 11
issuer_weid = "did:weid:0xfd28ad212a2de77fee518b4914b8579a40c601fa"
# expirationDate = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.localtime(time.time()))
expirationDate = "2021-04-18T21:12:33Z"

claim = {
            "name": "zhang san",
            "gender": "F",
            "age": 18
        }

# respBody = weid.create_credential_pojo(cptId, issuer_weid, expirationDate, claim)
# pprint(respBody)



weidentity = weidentityService(Config.get("LOCAL_WEID_URL"))
# expirationDate, claim, invokerWeId):
resp = weidentity.create_credential(cptId, issuerWeId=issuer_weid, expirationDate=expirationDate, claim=claim, invokerWeId=issuer_weid)
pprint(resp)

# 创建私钥
signning_key = SigningKey.generate(curve=SECP256k1)
privkey = signning_key.to_string()
# 创建公钥
verifing_key = signning_key.get_verifying_key()
publicKey = str(eval("0x" + verifing_key.to_string().hex()))
#encodeResponseStr:="+QHpjQwIVNLmsz//HyWaobqFF0h25/+FF0h25/+CAomAgLkBxGvzCg0AAAAAAAAAAAAAAADZrqqYL8Ieqa3a8J5PDGojoI0wagAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAYAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAX3cNtgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADFMjkwNTY3OTgwODU2MDYyNjc3MjI2MzcxMjU3MTQzNzEyNTQ5NzQyOTE0NjM5ODgxNTg3NzE4MDMxNzM2NTAzNDkyMTk1ODAwNzE5OTU3NjgwOTcxODA1NjMzNjA1MDA1ODAzMjU5OTc0MzUzNDUwNzQ2OTc0Mjc2NDY3MDk2MTEwMDI1NTI3NDc2NjE0ODA5NjY4MTA3MzU5MnwweGQ5YWVhYTk4MmZjMjFlYTlhZGRhZjA5ZTRmMGM2YTIzYTA4ZDMwNmEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACjE2MDE2Mzc4MTQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQGA"
print(publicKey)
# 获取 nonce
nonce = str(random.randint(1, 999999999999999999999999999999))
respBody = weid.create_weidentity_did_first(publicKey, nonce)
encode_transaction = respBody['respBody']['encodedTransaction']
# base64解密
transaction = base64_decode(encode_transaction)
# 获取hash
hashedMsg = Hash(transaction)
bytes_hashed = bytes(bytearray.fromhex(hashedMsg))
print(bytes_hashed)

print(binary_to_list(bytes_hashed))
signature = signning_key.sign(bytes_hashed)
print(signature)
transaction_encode = base64_encode(signature)
print(transaction_encode)
weid_second = weid.create_weidentity_did_second(nonce, data=respBody['respBody']['data'], signedMessage=transaction_encode)
print(weid_second)