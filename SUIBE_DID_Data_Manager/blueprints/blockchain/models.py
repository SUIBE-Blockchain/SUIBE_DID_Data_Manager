import datetime as dt

from SUIBE_DID_Data_Manager.database import (
    Column,
    Model,
    db,
)
from SUIBE_DID_Data_Manager.extensions import db

class CredentialPojo(db.Model):
    __tablename__ = "credential_pojo"

    credentialID = db.Column(db.String(88), primary_key=True,nullable=False)
    cptId = db.Column(db.Integer(), nullable=False)
    claim = db.Column(db.JSON, default={}, nullable=False)
    claim_id = db.Column(db.String(88), db.ForeignKey('did.did'))
    expirationDate = db.Column(db.Integer(), nullable=False)
    issuanceDate = db.Column(db.Integer(), nullable=False)
    proof = db.Column(db.JSON, default={}, nullable=False)
    type = db.Column(db.JSON, default=[], nullable=False)
    is_cochain = db.Column(db.Boolean, default=False, nullable=False)
    # 说明是否上链，True为上链了

    issuer_id = db.Column(db.String(88), nullable=False)