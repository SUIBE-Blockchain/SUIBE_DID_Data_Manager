from SUIBE_DID_Data_Manager.weidentity.weidentityClient import weidentityClient
from SUIBE_DID_Data_Manager.weidentity.weidentityService import weidentityService
from SUIBE_DID_Data_Manager.config import Config

import random
from ecdsa import SigningKey, SECP256k1
from eth_account import Account

from pprint import pprint
from SUIBE_DID_Data_Manager.weidentity.localweid import base64_decode, base64_encode, Hash

weid = weidentityService(Config.get("SERVER_WEID_URL"))
a = weid.create_weidentity_did()
print(a['respBody'])
b = weid.get_weidentity_did(a['respBody'])
pprint(b)

weid = weidentityClient(Config.get("LOCAL_WEID_URL"))
# 创建私钥
signning_key = SigningKey.generate(curve=SECP256k1)
print(signning_key,type(signning_key))
privkey = signning_key.to_string()
print(privkey)
# 创建公钥
verifing_key = signning_key.get_verifying_key()
publicKey = str(eval("0x" + verifing_key.to_string().hex()))
#encodeResponseStr:="+QHpjQwIVNLmsz//HyWaobqFF0h25/+FF0h25/+CAomAgLkBxGvzCg0AAAAAAAAAAAAAAADZrqqYL8Ieqa3a8J5PDGojoI0wagAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAYAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAX3cNtgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADFMjkwNTY3OTgwODU2MDYyNjc3MjI2MzcxMjU3MTQzNzEyNTQ5NzQyOTE0NjM5ODgxNTg3NzE4MDMxNzM2NTAzNDkyMTk1ODAwNzE5OTU3NjgwOTcxODA1NjMzNjA1MDA1ODAzMjU5OTc0MzUzNDUwNzQ2OTc0Mjc2NDY3MDk2MTEwMDI1NTI3NDc2NjE0ODA5NjY4MTA3MzU5MnwweGQ5YWVhYTk4MmZjMjFlYTlhZGRhZjA5ZTRmMGM2YTIzYTA4ZDMwNmEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACjE2MDE2Mzc4MTQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQGA"

# 获取 nonce
nonce = str(random.randint(1, 999999999999999999999999999999))
print(publicKey)
respBody = weid.create_weidentity_did_first("2905679808560626772263712571437125497429146398815877180317365034921958007199576809718056336050058032599743534507469742764670961100255274766148096681073592", nonce)
encode_transaction = respBody['respBody']['encodedTransaction']
print("1:"+encode_transaction)
# base64解密
transaction = base64_decode(respBody['respBody']['encodedTransaction'])
# 获取hash
print(transaction)
hashedMsg = Hash(transaction)
print(hashedMsg)
signature = signning_key.sign(bytes(hashedMsg, "utf-8"))
transaction_encode = base64_encode(signature)
print(transaction_encode)
weid_second = weid.create_weidentity_did_second(nonce, data=respBody['respBody']['data'], signedMessage=transaction_encode)
print(weid_second)