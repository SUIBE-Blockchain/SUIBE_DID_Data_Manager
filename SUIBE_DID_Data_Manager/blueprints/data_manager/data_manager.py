# -*- coding: utf-8 -*-
"""User views."""
from flask import Blueprint, render_template, jsonify
from flask_login import login_required

data_manager = Blueprint('data_manager', __name__)

@data_manager.route("/credential")
@login_required
def credential():
    data_dict = {
      "@context": "https://weidentity.webank.com/vc/v1",
      "id": "dsfewr23sdcsdfeqeddadfd",
      "type": ["Credential", "cpt100"],
      "issuer": "did:weid:1:0x2323e3e3dweweewew2www124151251",
      "issued": "2010-01-01T21:19:10Z",
      "claim": {
        "primeNumberIdx":"1234"
      },
      "revocation": {
        "id": "did:weid:1:2323e3e3dweweewew2",
        "type": "SimpleRevocationList2017"
      },
      "signature": [{
        "type": "LinkedDataSignature2015",
        "created": "2016-06-18T21:19:10Z",
        "creator": "did:weid:1:2323e3e3dweweewew2",
        "domain": "www.diriving_card.com",
        "nonce": "598c63d6",
        "signatureValue": "BavEll0/I1zpYw8XNi1bgVg/sCneO4Jugez8RwDg/+MCRVpjOboDoe4SxxKjkCOvKiCHGDvc4krqi6Z1n0UfqzxGfmatCuFibcC1wpsPRdW+gGsutPTLzvueMWmFhwYmfIFpbBu95t501+rSLHIEuujM/+PXr9Cky6Ed+W3JT24="
      }]
    }

    return jsonify(data_dict)