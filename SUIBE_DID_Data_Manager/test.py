from SUIBE_DID_Data_Manager.weidentity.weidentityClient import weidentityClient
from SUIBE_DID_Data_Manager.config import Config
from SUIBE_DID_Data_Manager.blockchain_utils.signtransaction import SignTx
import secp256k1prp
import os
import random
from pprint import pprint
weid = weidentityClient(Config.get("LOCAL_WEID_URL"))
publicKey = str(random.randint(1, 9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999))
nonce = str(random.randint(1, 999999999999999999999999999999))
a = weid.create_weidentity_did_first(publicKey, nonce)
pprint(a)
transaction_dict = {
    "encodedTransaction": a['respBody']['encodedTransaction']
}
sign = SignTx()
signmsg = sign.sign_transaction(transaction_dict=transaction_dict)

print()
print(signmsg)
weid_second = weid.create_weidentity_did_second(nonce, data=a['respBody']['data'], signedMessage="ODA5ODEyNjM4MjU2YzEyMzViMTIzMTAwMGUwMDAwMDAwMDEyMzEyODdiYWNmMjEzYw==")

# pprint(a)
print()
print(a['respBody']['data'])
print("=========================================================================")
print()
pprint(weid_second)
