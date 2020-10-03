from SUIBE_DID_Data_Manager.weidentity.weidentityClient import weidentityClient
from SUIBE_DID_Data_Manager.config import Config
import random
from ecdsa import SigningKey, SECP256k1

from pprint import pprint
from SUIBE_DID_Data_Manager.weidentity.localweid import base64_decode, base64_encode, Hash

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
transaction = base64_decode(respBody['respBody']['encodedTransaction'])
# 获取hash
hashedMsg = Hash(transaction)

signature = signning_key.sign(bytes(hashedMsg, "utf-8"))
transaction_encode = base64_encode(signature)
print(transaction_encode)
weid_second = weid.create_weidentity_did_second(nonce, data=respBody['respBody']['data'], signedMessage=transaction_encode)
pprint(weid_second)