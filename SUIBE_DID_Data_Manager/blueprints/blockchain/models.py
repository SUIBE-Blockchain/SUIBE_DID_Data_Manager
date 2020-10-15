import datetime as dt

from SUIBE_DID_Data_Manager.database import (
    Column,
    Model,
    db,
)
from SUIBE_DID_Data_Manager.blueprints.did_engine.models import DID


class CredentialPojo(Model):
    __tablename__ = "credential_pojo"

    id = db.Column(db.Integer, primary_key=True)
    credentialID = db.Column(db.String(88), nullable=False)
    cptId = db.Column(db.Integer(), nullable=False)
    claim = db.Column(db.JSON, default={}, nullable=False)
    expirationDate = db.Column(db.Integer(), nullable=False)
    # issuer = db.relationship(
    #     "DID",
    #     foreign_keys=[],
    #     primaryjoin="CredentialPojo.issuer == DID.id",
    #     backref="credential_pojo"
    #
    # )
    issuer = db.Column(db.String(88), nullable=False)
    issuanceDate = db.Column(db.Integer(), nullable=False)
    proof = db.Column(db.JSON, default={}, nullable=False)
    type = db.Column(db.JSON, default=[], nullable=True)