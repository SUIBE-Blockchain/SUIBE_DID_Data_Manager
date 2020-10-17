import datetime as dt

from SUIBE_DID_Data_Manager.database import (
    Column,
    Model,
    db,
)

from SUIBE_DID_Data_Manager.blueprints.blockchain.models import CredentialPojo
from SUIBE_DID_Data_Manager.blueprints.auth_manager.models import DataManager
from SUIBE_DID_Data_Manager.extensions import db


class DID(db.Model):
    __tablename__ = "did"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(22), nullable=False)
    did = db.Column(db.String(88), unique=True, nullable=False)
    type = db.Column(db.String(22), nullable=False)

    privkey_hex = db.Column(db.String(355), nullable=True)
    privkey_int = db.Column(db.String(355), nullable=True)

    publickey_hex = db.Column(db.String(355), nullable=True)
    publickey_int = db.Column(db.String(355), nullable=True)

    credential_pojo = db.relationship("CredentialPojo", backref="did")
    data_manager = db.relationship("DataManager", backref="did")
