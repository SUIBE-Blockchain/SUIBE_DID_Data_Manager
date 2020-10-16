from SUIBE_DID_Data_Manager.weidentity.weidentityClient import weidentityClient
from SUIBE_DID_Data_Manager.weidentity.weidentityService import weidentityService
from SUIBE_DID_Data_Manager.config import Config
from SUIBE_DID_Data_Manager.weidentity.localweid import generate_addr
import hashlib
import random
from ecdsa import SigningKey, SECP256k1
from eth_account import Account

from pprint import pprint
from SUIBE_DID_Data_Manager.weidentity.localweid import base64_decode, base64_encode, Hash
import time

weid = weidentityClient(Config.get("LOCAL_WEID_URL"))

# 创建私钥
# signning_key = SigningKey.generate(curve=SECP256k1)
# print()

priv_key = "18e14a7b6a307f426a94f8114701e7c8e774e7f9a47e2c2035db29a206321725"
signning_key = SigningKey.from_string(bytes.fromhex(priv_key), curve=SECP256k1)
privkey = signning_key.to_string()
# 创建公钥
verifing_key = signning_key.get_verifying_key()
publicKey = str(eval("0x" + verifing_key.to_string().hex()))
# 获取 nonce
nonce = str(random.randint(1, 999999999999999999999999999999))
respBody = weid.create_weidentity_did_first(publicKey, nonce)
print(respBody)
encode_transaction = respBody['respBody']['encodedTransaction']
# base64解密
transaction = base64_decode(encode_transaction)
# 获取hash
hashedMsg = Hash(transaction)
bytes_hashed = bytes(bytearray.fromhex(hashedMsg))
# 签名
signature = signning_key.sign(bytes_hashed, hashfunc=hashlib.sha256)

result = verifing_key.verify(signature=signature, data=bytes_hashed, hashfunc=hashlib.sha256)
print(result)
# base64加密
transaction_encode = base64_encode(signature)
weid_second = weid.create_weidentity_did_second(nonce, data=respBody['respBody']['data'], signedMessage=transaction_encode)
print(weid_second)